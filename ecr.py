import boto3
import json
import csv
import concurrent.futures
from tqdm import tqdm

print('''                                 
 .-----.----.----.                 
 |  -__|  __|   _|                 
 |_____|____|__|        
                 
 .--.--.-----.---.-.-----.-----.   
 |  |  |__ --|  _  |  _  |  -__|   
 |_____|_____|___._|___  |_____|   
                   |_____|    __   
 .----.-----.-----.-----.----|  |_ 
 |   _|  -__|  _  |  _  |   _|   _|
 |__| |_____|   __|_____|__| |____|
            |__|                   
                                    
''')

def get_repository_names(client):
    paginator = client.get_paginator('describe_repositories')
    repository_names = []
    for page in paginator.paginate():
        for repo in page['repositories']:
            repository_names.append(repo['repositoryName'])
    return repository_names

def get_lifecycle_policy(client, repository_name):
    try:
        response = client.get_lifecycle_policy(repositoryName=repository_name)
        policy = json.loads(response['lifecyclePolicyText'])  
        return policy['rules']
    except client.exceptions.LifecyclePolicyNotFoundException:
        return None

def get_images_and_size(client, repository_name):
    paginator = client.get_paginator('describe_images')
    image_details = []
    for page in paginator.paginate(repositoryName=repository_name):
        for image in page['imageDetails']:
            image_details.append(image)
    image_count = len(image_details)
    total_size = sum([img['imageSizeInBytes'] for img in image_details])
    return image_count, total_size

def process_repository(client, sts_client, account_id, repository_name):
    repo_info = {}
    
    lifecycle_policy = get_lifecycle_policy(client, repository_name)
    image_count, total_size_bytes = get_images_and_size(client, repository_name)
    total_size_mb = bytes_to_mb(total_size_bytes)
    total_size_gb = bytes_to_gb(total_size_bytes)
    total_size_tb = bytes_to_tb(total_size_bytes)
    tags = get_tags(client, repository_name, account_id)

    repo_info = {
        'name': repository_name,
        'lifecycle_policy': lifecycle_policy,
        'image_count': image_count,
        'total_size_bytes': total_size_bytes,
        'total_size_mb': total_size_mb,
        'total_size_gb': total_size_gb,
        'total_size_tb': total_size_tb,
        'tags': tags
    }

    return repo_info

def bytes_to_mb(bytes):
    return bytes / (1024 * 1024)

def bytes_to_gb(bytes):
    return bytes / (1024 * 1024 * 1024)

def bytes_to_tb(bytes):
    return bytes / (1024 * 1024 * 1024 * 1024)

def get_account_id(sts_client):
    caller_identity = sts_client.get_caller_identity()
    return caller_identity["Account"]

def get_tags(client, repository_name, account_id):
    region_name = client.meta.region_name
    response = client.list_tags_for_resource(
        resourceArn=f'arn:aws:ecr:{region_name}:{account_id}:repository/{repository_name}'
    )
    return response.get('tags', [])

def main():
    client = boto3.client('ecr')
    sts_client = boto3.client("sts")

    account_id = get_account_id(sts_client)
    repository_names = get_repository_names(client)

    print()
    print('Fetching repos metrics, statistics and tags:')

    repo_info = []
    total_repos = 0
    repos_without_tags = 0
    repos_without_policy = 0
    total_images = 0
    total_size_bytes_all_repos = 0

    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_repo = {executor.submit(process_repository, client, sts_client, account_id, repository_name): repository_name for repository_name in repository_names}
        for future in tqdm(concurrent.futures.as_completed(future_to_repo), total=len(repository_names), desc="", ncols=70):
            total_repos += 1
            try:
                result = future.result()
                repo_info.append(result)

                if not result['lifecycle_policy']:
                    repos_without_policy += 1
                total_images += result['image_count']
                total_size_bytes_all_repos += result['total_size_bytes']
                if not result['tags']:
                    repos_without_tags += 1
                
            except Exception as exc:
                print('%r generated an exception: %s' % (future_to_repo[future], exc))
            else:
                print('%r page is %d bytes' % (future_to_repo[future], len(result)))
    
        repo_info.sort(key=lambda x: x['total_size_bytes'], reverse=True)

        fieldnames = ['name', 'lifecycle_policy', 'image_count', 'total_size_bytes', 'total_size_mb', 'total_size_gb', 'total_size_tb', 'tags']
        with open('repo_info.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for repo in repo_info:
                print(f'Repository: {repo["name"]}')
                print(f'Lifecycle Policy: {repo["lifecycle_policy"]}')
                print(f'Number of Images: {repo["image_count"]}')
                print(f'Total Size: {repo["total_size_bytes"]:.3f} bytes ({repo["total_size_mb"]:.3f} MB) ({repo["total_size_gb"]:.3f} GB) ({repo["total_size_tb"]:.3f} TB' )
                print('Tags:')
                for tag in repo['tags']:
                    print(f'  {tag["Key"]}: {tag["Value"]}')
                print()
                writer.writerow({
                    'name': repo['name'],
                    'lifecycle_policy': json.dumps(repo['lifecycle_policy']),
                    'image_count': repo['image_count'],
                    'total_size_bytes': repo['total_size_bytes'],
                    'total_size_mb': repo['total_size_mb'],
                    'total_size_gb': repo['total_size_gb'],
                    'total_size_tb': repo['total_size_tb'],
                    'tags': json.dumps(repo['tags'])
                })

            print("""
Summary Report:
Total size of all repositories: 
{:.3f} TB
{:.3f} GB
{:.3f} MB
{:.3f} bytes 

""".format(
    bytes_to_tb(total_size_bytes_all_repos),
    bytes_to_gb(total_size_bytes_all_repos),
    bytes_to_mb(total_size_bytes_all_repos),
    total_size_bytes_all_repos
).strip())
            print()
            print('Top 10 biggest repositories by size:')
            for i, repo in enumerate(repo_info[:10]):
                print(f'{i+1}. {repo["name"]} - {repo["image_count"]} images - {repo["total_size_bytes"]:.3f} bytes ({repo["total_size_mb"]:.3f} MB) ({repo["total_size_gb"]:.3f} GB) ({repo["total_size_tb"]:.3f} TB) ')

            with open('repo_info.json', 'w') as f:
                json.dump(repo_info, f, indent=4, sort_keys=True, default=str)
        print()
        print('Statistics:')
        print(f'Total number of repositories: {total_repos}')
        print(f'Total number of images across all repositories: {total_images}') 
        print(f'Number of repositories without tags: {repos_without_tags}')
        print(f'Number of repositories without lifecycle policies: {repos_without_policy}')

if __name__ == "__main__":
    main()