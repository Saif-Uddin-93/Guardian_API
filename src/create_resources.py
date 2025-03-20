from utility.aws_utils import *


iam_role_id, iam_role_arn = create_iam_role()
create_sqs_queue("guardian-queue")
create_api("guardian-api")
create_lambda()