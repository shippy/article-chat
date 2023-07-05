terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

# Configure the AWS Provider
provider "aws" {
  region = "eu-central-1"
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

# Create a backend S3 bucket to store Terraform state
resource "aws_s3_bucket" "terraform-state" {
  bucket = "terraform-state"
}

