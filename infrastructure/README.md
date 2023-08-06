## Infrastructure

This directory contains the Terraform code for the infrastructure that powers the site.

### Setup

1. Create a Terraform Cloud project and set it to only store state.
2. Change the AWS profile name in `main.tf`. (TODO: Move out into `tfvars`)

### Diagram

```mermaid
graph TB
  terraform{{Terraform}}

  subgraph AWS_Cloud
    subgraph VPC
      route53[Route 53]
      acm[ACM]
      rds[RDS Postgres + pgvector]
      ecr[ECS via ECR]
      alb[ALB]
      s3[S3]
      cloudfront[Cloudfront]
      iam[IAM Policies]
    end
  end
  
  subgraph Github
    github_actions[GitHub Actions]
  end
  
  subgraph Namecheap
    namecheap[Namecheap Domain]
  end

  subgraph OpenAI
    openai[OpenAI API]
  end

  %% Define dependencies.
  terraform-->|Provisions|route53
  terraform-->|Provisions|acm
  terraform-->|Provisions|rds
  terraform-->|Provisions|ecr
  terraform-->|Provisions|alb
  terraform-->|Provisions|s3
  terraform-->|Provisions|cloudfront
  terraform-->|Provisions|iam
  route53-->|Manages DNS for|namecheap
  github_actions-->|Pushes to|ecr
  github_actions-->|Updates and Invalidates|s3
  acm-->|SSL for|namecheap
  ecr-->|Deploys to|alb
  alb-->|Balances Load For|rds
  s3-->|Serves|cloudfront
  ecr-->|Queries|openai
  iam-->|Policies for|ecr
  iam-->|Policies for|rds
  iam-->|Policies for|s3
  iam-->|Policies for|cloudfront
  iam-->|Policies for|acm
```