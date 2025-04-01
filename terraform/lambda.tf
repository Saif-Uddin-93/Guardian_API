resource "aws_lambda_layer_version" "requests_layer" {
  layer_name               = "requests"
  filename                 = "${path.module}/../requests_layer.zip"
  compatible_runtimes      = ["python3.13"]
  compatible_architectures = ["arm64", "x86_64"]
  description              = "Requests layer for Lambda functions"
}

resource "aws_lambda_layer_version" "utility_layer" {
  layer_name               = "utility"
  filename                 = "${path.module}/../utility_layer.zip"
  compatible_runtimes      = ["python3.13"]
  compatible_architectures = ["arm64", "x86_64"]
  description              = "Utility layer for Lambda functions"
}

data "archive_file" "sqs_send_lambda" {
  type             = "zip"
  source_file      = "${path.module}/../lambda_handlers/sqs_send.py"
  output_file_mode = "0666"
  output_path      = "${path.module}/../lambda_handlers/sqs_send.zip"
}

data "archive_file" "sqs_receive_lambda" {
  type             = "zip"
  source_file      = "${path.module}/../lambda_handlers/sqs_receive.py"
  output_file_mode = "0666"
  output_path      = "${path.module}/../lambda_handlers/sqs_receive.zip"
}

resource "aws_lambda_function" "sqs_send_lambda" {
  filename         = "${path.module}/../lambda_handlers/sqs_send.zip"
  function_name    = "sqs_send"
  role             = aws_iam_role.lambda_iam_role.arn
  handler          = "sqs_send.lambda_handler"
#   source_code_hash = data.archive_file.sqs_send_lambda.output_base64sha256
  runtime          = "python3.13"
  timeout          = 10
  layers           = [
    aws_lambda_layer_version.requests_layer.arn,
    aws_lambda_layer_version.utility_layer.arn,
  ]
  tracing_config {
    mode = "PassThrough"
  }
  logging_config {
    log_format = "Text"
    log_group  = "/aws/lambda/guardian_sqs_send"
  }
  ephemeral_storage {
    size = 512
  }
}

resource "aws_lambda_function" "sqs_receive_lambda" {
  filename         = "${path.module}/../lambda_handlers/sqs_receive.zip"
  function_name    = "sqs_receive"
  role             = aws_iam_role.lambda_iam_role.arn
  handler          = "sqs_receive.lambda_handler"
#   source_code_hash = data.archive_file.sqs_receive_lambda.output_base64sha256
  runtime          = "python3.13"
  timeout          = 10
  layers           = [
    aws_lambda_layer_version.utility_layer.arn,
  ]
  tracing_config {
    mode = "PassThrough"
  }
  logging_config {
    log_format = "Text"
    log_group  = "/aws/lambda/sqs_receive"
  }
  ephemeral_storage {
    size = 512
  }
}
