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

resource "aws_lambda_function" "sqs_receive_lambda" {
  filename         = "${path.module}/../lambda_handlers/sqs_receive.zip"
  function_name    = "sqs_receive"
  role             = aws_iam_role.guardian_iam_role.arn
  handler          = "sqs_receive.lambda_handler"
  source_code_hash = data.archive_file.sqs_receive_lambda.output_base64sha256
  runtime          = "python3.13"
  timeout          = 60
  layers           = [
    aws_lambda_layer_version.utility_layer.arn,
  ]
}

# {
#     "FunctionName": "LambdaTest",
#     "FunctionArn": "arn:aws:lambda:eu-west-2:841162707768:function:LambdaTest",
#     "Runtime": "python3.13",
#     "Role": "arn:aws:iam::841162707768:role/guardian-iam-role",
#     "Handler": "lambda_function.lambda_handler",
#     "CodeSize": 798,
#     "Description": "",
#     "Timeout": 3,
#     "MemorySize": 128,
#     "LastModified": "2025-03-21T02:21:42.000+0000",
#     "CodeSha256": "ex66Ki3Ie+SEFW1eqStQzRDzr7cRaVtJgNRI/FEYFOA=",
#     "Version": "$LATEST",
#     "TracingConfig": {
#         "Mode": "PassThrough"
#     },
#     "RevisionId": "af4f48fd-10b3-489f-ae7a-aed7a2823376",
#     "Layers": [
#         {
#             "Arn": "arn:aws:lambda:eu-west-2:841162707768:layer:requests:2",
#             "CodeSize": 1083000
#         },
#         {
#             "Arn": "arn:aws:lambda:eu-west-2:841162707768:layer:utility:9",
#             "CodeSize": 14496
#         }
#     ],
#     "PackageType": "Zip",
#     "Architectures": [
#         "x86_64"
#     ],
#     "EphemeralStorage": {
#         "Size": 512
#     },
#     "SnapStart": {
#         "ApplyOn": "None",
#         "OptimizationStatus": "Off"
#     },
#     "LoggingConfig": {
#         "LogFormat": "Text",
#         "LogGroup": "/aws/lambda/LambdaTest"
#     }
# }