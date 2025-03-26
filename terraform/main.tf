terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "eu-west-2"
  default_tags {
    tags = {
      ProjectName  = "Launchpad DE - Guardian API"
      Team         = "Stray Tech"
      TeamMembers  = "Saif Uddin"
      DeployedFrom = "Terraform"
      Repository   = "https://github.com/Saif-Uddin-93/Guardian_API"
      CostCentre   = "DE"
      Environment  = "dev"
    }
  }
}

data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

locals {
  account_id = data.aws_caller_identity.current.account_id
  region = data.aws_region.current.name
}