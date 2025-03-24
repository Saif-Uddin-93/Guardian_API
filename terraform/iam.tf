locals {
  account_id = data.aws_caller_identity.current.account_id
}

resource "aws_iam_role" "lambda_iam_role" {
  name = "lambda-iam-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
          AWS     = "arn:aws:iam::${local.account_id}:root"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_policy" "lambda_permissions_policy" {
  name        = "lambda_iam_policy"
  description = "Permissions policy for lambda"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = [
          "lambda:*",
        ]
        Resource = [
          "${aws_lambda_function.sqs_receive_lambda.arn}",
          "${aws_lambda_function.sqs_send_lambda.arn}",
        ]
      }
    ]
  })
}

resource "aws_iam_role" "sqs_iam_role" {
  name = "sqs_iam_role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "sqs.amazonaws.com"
          AWS     = "arn:aws:iam::${local.account_id}:root"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_policy" "sqs_permissions_policy" {
  name        = "sqs-iam-policy"
  description = "Permissions policy for Guardian IAM role"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = [
          "sqs:*"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role" "apigw_iam_role" {
  name = "apigw-iam-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "apigateway.amazonaws.com"
          AWS     = "arn:aws:iam::${local.account_id}:root"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_policy" "apigw_permissions_policy" {
  name        = "apigw-iam-policy"
  description = "Permissions policy for apigw IAM role"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = [
          "apigateway:*"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "guardian_lambda_full" {
  role       = aws_iam_role.lambda_iam_role.name
  policy_arn = "arn:aws:iam::aws:policy/AWSLambda_FullAccess"
}

resource "aws_iam_role_policy_attachment" "guardian_lambda" {
  role       = aws_iam_role.lambda_iam_role.name
  policy_arn = aws_iam_policy.lambda_permissions_policy.arn
}

resource "aws_iam_role_policy_attachment" "guardian_apigateway_full" {
  role       = aws_iam_role.apigw_iam_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonAPIGatewayAdministrator"
}

resource "aws_iam_role_policy_attachment" "guardian_apigateway" {
  role       = aws_iam_role.apigw_iam_role.name
  policy_arn = aws_iam_policy.apigw_permissions_policy.arn
}

resource "aws_iam_role_policy_attachment" "guardian_sqs_full" {
  role       = aws_iam_role.sqs_iam_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSQSFullAccess"
}

resource "aws_iam_role_policy_attachment" "guardian_sqs" {
  role       = aws_iam_role.sqs_iam_role.name
  policy_arn = aws_iam_policy.sqs_permissions_policy.arn
}

# resource "aws_iam_role_policy_attachment" "guardian_custom_policy" {
#   role       = aws_iam_role.guardian_iam_role.name
#   policy_arn = aws_iam_policy.guardian_permissions_policy.arn
# }

data "aws_iam_policy_document" "sqs_policy_doc" {
  statement {
    principals {
      type        = "*"
      identifiers = ["*"]
    }

    actions       = ["sqs:*"]
    resources     = [aws_sqs_queue.guardian_queue.arn]
  }
}