terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
  
  # cloud {
  #   organization = "simonpodhajsky"

  #   workspaces {
  #     name = "article-chat"
  #   }
  # }

  # backend "s3" {
  #   bucket = "chatarticle-terraform-state"
  #   key    = "terraform.tfstate"
  #   region = "eu-central-1"
  # }
}

# Configure the AWS Provider
provider "aws" {
  region = var.aws_region
  shared_config_files = [ "~/.aws/config" ]
  shared_credentials_files = [ "~/.aws/credentials" ]
  profile = "AdministratorAccess-637364745310"

  default_tags {
    tags = {
      Terraform = "true"
      ArticleChat = "true"
    }
  }
}

# # Create a backend S3 bucket to store Terraform state
# resource "aws_s3_bucket" "terraform-state" {
#   bucket = "chatarticle-terraform-state"
# }

# resource "aws_s3_bucket_versioning" "terraform-state-versioning" {
#   bucket = "chatarticle-terraform-state"
#   versioning_configuration {
#     status = "Enabled"
#   }
# }