provider "aws" {
  region = "eu-west-2"
}

resource "aws_iam_role" "guardian_iam_role" {
  name = "guardian-iam-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_policy" "guardian_permissions_policy" {
  name        = "guardian-iam-policy"
  description = "Permissions policy for Guardian IAM role"
  
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = [
          "apigateway:*",
          "lambda:*",
          "sqs:CreateQueue",
          "sqs:GetQueueAttributes",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "guardian_lambda_full" {
  role       = aws_iam_role.guardian_iam_role.name
  policy_arn = "arn:aws:iam::aws:policy/AWSLambda_FullAccess"
}

resource "aws_iam_role_policy_attachment" "guardian_apigateway_full" {
  role       = aws_iam_role.guardian_iam_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonAPIGatewayAdministrator"
}

resource "aws_iam_role_policy_attachment" "guardian_sqs_full" {
  role       = aws_iam_role.guardian_iam_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSQSFullAccess"
}

resource "aws_iam_role_policy_attachment" "guardian_custom_policy" {
  role       = aws_iam_role.guardian_iam_role.name
  policy_arn = aws_iam_policy.guardian_permissions_policy.arn
}
