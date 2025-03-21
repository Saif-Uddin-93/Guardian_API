resource "aws_lambda_layer_version" "requests_layer" {
  layer_name          = "requests_layer"
  filename            = "${path.module}/../requests_layer.zip"
}

resource "aws_lambda_layer_version" "utility_layer" {
  layer_name          = "utility_layer"
  filename            = "${path.module}/../utility_layer.zip"
}

data "archive_file" "sqs_send_lambda" {
  type             = "zip"
  source_file      = "${path.module}/../lambda_handlers/sqs_send.py"
  output_file_mode = "0666"
  output_path      = "${path.module}/../lambda_handlers/sqs_send.zip"
}

resource "aws_lambda_function" "sqs_send_lambda" {
  filename         = "${path.module}/../lambda_handlers/sqs_send.zip"
  function_name    = "sqs_send"
  role             = aws_iam_role.guardian_iam_role.arn
  handler          = "sqs_send.lambda_handler"
  source_code_hash = data.archive_file.sqs_send_lambda.output_base64sha256
  runtime          = "python3.13"
  timeout          = 60
  layers           = [
    aws_lambda_layer_version.requests_layer.arn,
    aws_lambda_layer_version.utility_layer.arn,
  ]
}