resource "aws_cloudwatch_log_group" "apigw_log_group" {
  name              = "/aws/apigateway/guardian-api"
  retention_in_days = 30
}

resource "aws_cloudwatch_log_group" "sqs_send_log_group" {
  name              = "/aws/lambda/guardian_sqs_send"
  retention_in_days = 30
}

resource "aws_cloudwatch_log_group" "sqs_receive_log_group" {
  name              = "/aws/lambda/guardian_sqs_receive"
  retention_in_days = 30
}

resource "aws_cloudwatch_log_stream" "apigw_log_stream" {
  name           = "apigw_log_stream"
  log_group_name = aws_cloudwatch_log_group.apigw_log_group.name
}

resource "aws_cloudwatch_log_stream" "sqs_send_log_stream" {
  name           = "sqs_send_log_stream"
  log_group_name = aws_cloudwatch_log_group.sqs_send_log_group.name
}

resource "aws_cloudwatch_log_stream" "sqs_receive_log_stream" {
  name           = "sqs_receive_log_stream"
  log_group_name = aws_cloudwatch_log_group.sqs_receive_log_group.name
}
