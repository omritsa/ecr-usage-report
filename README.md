# AWS ECR Usage Report

## Introduction

AWS ECR (Elastic Container Registry) is a fully-managed Docker container registry that makes it easy for developers to store, manage, and deploy Docker container images. AWS ECR is integrated with Amazon Elastic Container Service (ECS), simplifying your development to production workflow. 

As the usage of AWS ECR increases, it can become challenging to keep track of the images, their versions, and their sizes. This becomes even more important when costs are a factor. The cost of AWS ECR is directly proportional to the amount of data stored and the number of data transfer operations. Therefore, tracking this usage becomes very important to managing costs.

This Python script helps DevOps and FinOps engineers by providing a usage report against AWS ECR. The script fetches metrics, statistics, and tags for each repository, helping you keep track of your repositories' size and apply lifecycle policies where necessary.

## Features

The script provides the following details:

- Total size of all repositories
- Total number of repositories
- Total number of images across all repositories
- Number of repositories without tags
- Number of repositories without lifecycle policies
- Top 10 biggest repositories by size
- Detailed view of each repository, including:
  - Name
  - Lifecycle policy
  - Number of images
  - Total size
  - Tags

The script also saves a full report of its finding in a csv and json format.

## Requirements

- Python 3.x
- AWS CLI configured with necessary permissions

## Usage

1. Clone this repository:
```bash
git clone https://github.com/username/repository.git
cd repository
pip3 install boto3 tqdm
```

2. Run the script:
```bash
python3 ecr.py
```

## Output

The script will output a detailed report of your AWS ECR usage. Here is a sample output:

```shell
Fetching repos metrics, statistics and tags:
  0%|                                           | 0/2 [00:00<?, ?it/s]'new' page is 8 bytes
  50%|█████████████████▌                 | 1/2 [00:00<00:00,  1.89it/s]'test' page is 8 bytes
  100%|███████████████████████████████████| 2/2 [00:01<00:00,  1.97it/s]
  
Repository: new
Lifecycle Policy: None
Number of Images: 1
Total Size: 78531277.000 bytes (74.893 MB) (0.073 GB) (0.000 TB)
Tags:
  name: temp
  env: dev

Repository: test
Lifecycle Policy: [{'rulePriority': 1, 'description': 'remove alpha images', 'selection': {'tagStatus': 'any', 'countType': 'sinceImagePushed', 'countUnit': 'days', 'countNumber': 1}, 'action': {'type': 'expire'}}]
Number of Images: 0
Total Size: 0.000 bytes (0.000 MB) (0.000 GB) (0.000 TB)
Tags:
  name: test-repo
  env: dev

Summary Report:
Total size of all repositories: 
0.000 TB
0.073 GB
74.893 MB
78531277.000 bytes

Top 10 biggest repositories by size:
1. new - 1 images - 78531277.000 bytes (74.893 MB) (0.073 GB) (0.000 TB) 
2. test - 0 images - 0.000 bytes (0.000 MB) (0.000 GB) (0.000 TB) 

Statistics:
Total number of repositories: 2
Total number of images across all repositories: 1
Number of repositories without tags: 0
Number of repositories without lifecycle policies: 1
```

## Contributing

Your contributions are always welcome! Please take a look at the [contribution guidelines](CONTRIBUTING.md) first.

## License

This script is distributed under the Apache License 2.0, see [LICENSE](LICENSE.md) for more information.
