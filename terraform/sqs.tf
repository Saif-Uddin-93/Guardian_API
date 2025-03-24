resource "aws_sqs_queue" "guardian_queue" {
  name                        = "guardian-queue.fifo"
  fifo_queue                  = true
  message_retention_seconds   = 259200  # Retain messages for 3 days
  delay_seconds               = 0       # No delay before sending messages
  content_based_deduplication = true    # Enables automatic deduplication

  tags = {
    Environment = "dev"
  }
}


resource "aws_sqs_queue_policy" "guardian_queue_policy" {
  queue_url = aws_sqs_queue.guardian_queue.id
  policy    = data.aws_iam_policy_document.sqs_policy_doc.json
}