# ---------------
# Lambda IAM Role
# ---------------

# Define
data "aws_iam_policy_document" "sqs_policy_document" {
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

# Create
resource "aws_iam_policy" "sqs_policy" {
  name_prefix = "sqs-policy-"
  policy      = data.aws_iam_policy_document.sqs_policy_document.json
}

# Attach
resource "aws_iam_role_policy_attachment" "extract_secrets_manager_policy_attachment" {
  role       = aws_iam_role.extract_lambda_role.name
  policy_arn = aws_iam_policy.extract_secrets_manager_policy.arn
}