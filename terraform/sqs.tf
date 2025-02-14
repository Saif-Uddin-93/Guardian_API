resource "aws_sqs_queue" "terraform_queue" {
  name                      = "sqs-queue"
  # delay_seconds             = 90
  max_message_size          = 262144 # 256 kb
  message_retention_seconds = 259200 # 3 days
  receive_wait_time_seconds = 5

  tags = {
    Environment = "dev"
  }
}