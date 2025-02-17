resource "aws_iam_role" "sqs_lambda_role" {
  name_prefix        = "role-${var.extract_lambda}"
  assume_role_policy = data.aws_iam_policy_document.trust_policy.json
}



data "aws_iam_policy_document" "sqs_actions_policy" {
  statement {
    # sid    = "sqs_actions"
    effect = "Allow"

    actions   = [
        "sqs:CreateQueue",
        "sqs:GetQueueUrl",
        "sqs:SendMessage",
        "sqs:ReceiveMessage"
        ]
    resources = ["*"]
  }
}


resource "aws_iam_policy" "extract_secrets_manager_policy" {
  name_prefix = "sqs-policy-send-receive-"
  policy      = data.aws_iam_policy_document.sqs_actions_policy.json
}

# Attach
resource "aws_iam_role_policy_attachment" "extract_secrets_manager_policy_attachment" {
  role       = aws_iam_role.extract_lambda_role.name
  policy_arn = aws_iam_policy.extract_secrets_manager_policy.arn
}