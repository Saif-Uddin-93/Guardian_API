resource "aws_s3_bucket" "env_vars_bucket" {
  bucket        = var.env_vars_bucket
  force_destroy = true
  tags = {
    Name = "env-vars-bucket"
  }
}
