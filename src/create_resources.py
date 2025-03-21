from utility.aws_utils import *

create_sqs_queue("guardian-queue")
create_api("guardian-api")
create_lambda()