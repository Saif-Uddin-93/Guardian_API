terraform {

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket = "launchpad-saif-de-env-vars-bucket"
    key    = "terraform/terraform.tfstate"
    region = "eu-west-2"
  }
}

provider "aws" {
  region = "eu-west-2"
  default_tags {
    tags = {
      ProjectName  = "Launchpad DE Project - Saif"
      DeployedFrom = "Terraform"
      Repository   = "https://github.com/Saif-Uddin-93/"
      CostCentre   = "DE"
      Environment  = "dev"
    }
  }
}

data "aws_caller_identity" "current" {}
