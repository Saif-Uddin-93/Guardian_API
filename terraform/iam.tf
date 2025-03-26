# resource "aws_iam_role" "lambda_iam_role" {
#   name = "lambda-iam-role"

#   assume_role_policy = jsonencode({
#     Version = "2012-10-17"
#     Statement = [
#       {
#         Effect = "Allow"
#         Principal = {
#           Service = "lambda.amazonaws.com"
#           AWS     = "arn:aws:iam::${local.account_id}:root"
#         }
#         Action = "sts:AssumeRole"
#       }
#     ]
#   })
# }

resource "aws_iam_role" "lambda_role" {
  assume_role_policy = data.aws_iam_policy_document.lambda_policy_doc.json
}


resource "aws_iam_policy" "lambda_trust_policy" {
  name        = "lambda_iam_policy"
  description = "trust policy for lambda"
  
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
          "*"
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

resource "aws_iam_policy" "sqs_policy" {
  name_prefix = "sqs-policy"
  policy      = data.aws_iam_policy_document.sqs_policy_doc.json
}

# Attach
resource "aws_iam_role_policy_attachment" "sqs_policy_attachment" {
  role       = aws_iam_role.sqs_iam_role.name
  policy_arn = aws_iam_policy.sqs_policy.arn
}

resource "aws_iam_policy" "sqs_trust_policy" {
  name        = "sqs-iam-policy"
  description = "trust policy for Guardian IAM role"
  
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

resource "aws_iam_policy" "apigw_trust_policy" {
  name        = "apigw-iam-policy"
  description = "trust policy for apigw IAM role"
  
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
  policy_arn = aws_iam_policy.lambda_trust_policy.arn
}

resource "aws_iam_role_policy_attachment" "guardian_apigateway_full" {
  role       = aws_iam_role.apigw_iam_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonAPIGatewayAdministrator"
}

resource "aws_iam_role_policy_attachment" "guardian_apigateway" {
  role       = aws_iam_role.apigw_iam_role.name
  policy_arn = aws_iam_policy.apigw_trust_policy.arn
}

resource "aws_iam_role_policy_attachment" "apigw_logs" {
  role       = aws_iam_role.apigw_iam_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonAPIGatewayPushToCloudWatchLogs"
}

data "aws_iam_policy_document" "send_cw_policy_doc" {
  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = [
      "arn:aws:logs:${local.region}:${local.account_id}:log-group:${aws_cloudwatch_log_group.sqs_send_log_group.name}"
    ]
    effect = "Allow"
  }
}

data "aws_iam_policy_document" "lambda_policy_doc" {
  statement {
    effect = "Allow"
    # principals {
    #   type        = "Service"
    #   identifiers = ["lambda.amazonaws.com"]
    # }

    actions       = ["lambda:*"]
    # actions       = ["sts:AssumeRole"]
    resources     = ["*"]
  }
}

data "aws_iam_policy_document" "sqs_policy_doc" {
  statement {
    effect = "Allow"
    # principals {
    #   type        = "Service"
    #   identifiers = ["sqs.amazonaws.com"]
    # }

    actions       = ["sqs:*"]
    # actions       = ["sts:AssumeRole"]
    resources     = ["*"]
  }
}

resource "aws_iam_role_policy_attachment" "guardian_sqs_full" {
  role       = aws_iam_role.sqs_iam_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonSQSFullAccess"
}

resource "aws_iam_role_policy_attachment" "guardian_sqs" {
  role       = aws_iam_role.sqs_iam_role.name
  policy_arn = aws_iam_policy.sqs_trust_policy.arn
}

resource "aws_lambda_permission" "apigw_send" {
  statement_id  = "AllowExecutionFromAPIGatewaySend"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.sqs_send_lambda.arn
  principal     = "apigateway.amazonaws.com"

  source_arn = "arn:aws:execute-api:eu-west-2:${local.account_id}:${aws_api_gateway_rest_api.guardian_api.id}/*/*"
}

resource "aws_lambda_permission" "apigw_receive" {
  statement_id  = "AllowExecutionFromAPIGatewayReceive"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.sqs_receive_lambda.arn
  principal     = "apigateway.amazonaws.com"

  source_arn = "arn:aws:execute-api:eu-west-2:${local.account_id}:${aws_api_gateway_rest_api.guardian_api.id}/*/*"
}

# resource "aws_iam_role_policy_attachment" "guardian_custom_policy" {
#   role       = aws_iam_role.guardian_iam_role.name
#   policy_arn = aws_iam_policy.guardian_trust_policy.arn
# }