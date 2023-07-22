# AWS ECR Usage Report

```    
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
               
```                                    

## Introduction

AWS ECR (Elastic Container Registry) is a fully-managed Docker container registry that makes it easy for developers to store, manage, and deploy Docker container images.

As the usage of AWS ECR increases, it can become challenging to keep track of the images, their versions, and their sizes. This becomes even more important when costs are a factor. The cost of AWS ECR is directly proportional to the amount of data stored and the number of data transfer operations. Therefore, tracking this usage becomes very important to managing costs.

This Python script helps DevOps and FinOps professionals by providing a detailed usage report for AWS ECR. 
The script fetches metrics, statistics, and tags for each repository, helping you keep track of your repositories' size and apply lifecycle policies where necessary.

## What's the purpose of this code?

This code will provide you with the insights you need to reduce your AWS ECR costs.

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
git clone https://github.com/omritsa/ecr-usage-report.git
cd ecr-usage-report
pip3 install boto3 tqdm
```

2. Run the script:
```bash
python3 ecr.py
```

## Report Insights
```shell
Summary Report:
230 TB
234,970 GB
240,609,190 MB

Top 10 biggest repositories by size:
1. ****** - 8003 images - 11948202175781.000 bytes (11394693.542 MB) (11127.630 GB) (10.867 TB)
2. ****** - 13691 images - 11101059770565.000 bytes (10586795.588 MB) (10338.668 GB) (10.096 TB)
3. ****** - 5241 images - 4439289509626.000 bytes (4233636.388 MB) (4134.411 GB) (4.038 TB)
4. ****** - 5236 images - 4436746504394.000 bytes (4231211.190 MB) (4132.042 GB) (4.035 TB)
5. ****** - 5241 images - 4427730921886.000 bytes (4222613.260 MB) (4123.646 GB) (4.027 TB)
6. ****** - 5237 images - 4424471206107.000 bytes (4219504.553 MB) (4120.610 GB) (4.024 TB)
7. ****** - 5238 images - 4422046565896.000 bytes (4217192.236 MB) (4118.352 GB) (4.022 TB)
8. ****** - 5236 images - 4420372283795.000 bytes (4215595.516 MB) (4116.792 GB) (4.020 TB)
9. ****** - 5244 images - 4342904000412.000 bytes (4141716.004 MB) (4044.645 GB) (3.950 TB)
10. ****** - 5145 images - 4325751640618.000 bytes (4125358.239 MB) (4028.670 GB) (3.934 TB)

Statistics:
Total number of repositories: 203
Total number of images across all repositories: 314,043
Number of repositories without tags: 101
Number of repositories without lifecycle policies: 85
```

## Full Output

The script will output a detailed report of your AWS ECR usage. Here is a sample output:

```shell
omrits@Laptop ecr-usage-report % python3 ecr.py                          
                                 
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
