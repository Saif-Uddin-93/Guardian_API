mock_provider "aws" {
  region = "eu-west-2"
  default_tags {
    tags = {
      ProjectName  = "Launchpad DE Project - Saif"
      DeployedFrom = "Terraform"
      Repository   = "https://github.com/Shuhaan/project-onyx"
      CostCentre   = "DE"
      Environment  = "dev"
    }
  }
}

data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

module "extract" {
  source                  = "./extract"
  extract_lambda_role_arn = aws_iam_role.extract_lambda_role.arn
}

module "transform" {
  source                    = "./transform"
  ingested_data_bucket_arn  = aws_s3_bucket.ingested_data_bucket.arn
  transform_lambda_role_arn = aws_iam_role.transform_lambda_role.arn
}

module "load" {
  source                    = "./load"
  processed_data_bucket_arn = aws_s3_bucket.processed_data_bucket.arn
  load_lambda_role_arn      = aws_iam_role.load_lambda_role.arn
}