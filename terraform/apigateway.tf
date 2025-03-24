resource "aws_api_gateway_rest_api" "guardian_api" {
  name        = "guardian-api"
  description = "REST API to retrieve guardian data"

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

resource "aws_api_gateway_resource" "guardian_resource" {
  rest_api_id = aws_api_gateway_rest_api.guardian_api.id
  parent_id   = aws_api_gateway_rest_api.guardian_api.root_resource_id
  path_part   = "data"
}

resource "aws_api_gateway_method" "guardian_method" {
  rest_api_id   = aws_api_gateway_rest_api.guardian_api.id
  resource_id   = aws_api_gateway_resource.guardian_resource.id
  http_method   = "GET"
  authorization = "NONE"

  request_parameters = {
    "method.request.querystring.query"        = true
    "method.request.querystring.queue-name"   = true
    "method.request.querystring.from-date"    = false
    "method.request.querystring.to-date"      = false
    "method.request.querystring.page-size"    = false
    "method.request.querystring.star-rating"  = false
  }
}

resource "aws_api_gateway_integration" "guardian_integration" {
  rest_api_id             = aws_api_gateway_rest_api.guardian_api.id
  resource_id             = aws_api_gateway_resource.guardian_resource.id
  http_method             = aws_api_gateway_method.guardian_method.http_method
  integration_http_method = "PUT"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.sqs_send_lambda.invoke_arn

  request_templates = {
    "application/json" = <<EOT
#set($allParams = $input.params())
{
  "status" : "200",
  "body-json" : $input.json('$'),
  "params" : {
    #foreach($type in $allParams.keySet())
      #set($params = $allParams.get($type))
      "$type" : {
        #foreach($paramName in $params.keySet())
          "$paramName" : "$util.escapeJavaScript($params.get($paramName))"
          #if($foreach.hasNext),#end
        #end
      }
      #if($foreach.hasNext),#end
    #end
  },
  "stage-variables" : {
    #foreach($key in $stageVariables.keySet())
      "$key" : "$util.escapeJavaScript($stageVariables.get($key))"
      #if($foreach.hasNext),#end
    #end
  },
  "context" : {
    "account-id" : "$context.identity.accountId",
    "api-id" : "$context.apiId",
    "api-key" : "$context.identity.apiKey",
    "authorizer-principal-id" : "$context.authorizer.principalId",
    "caller" : "$context.identity.caller",
    "cognito-authentication-provider" : "$context.identity.cognitoAuthenticationProvider",
    "cognito-authentication-type" : "$context.identity.cognitoAuthenticationType",
    "cognito-identity-id" : "$context.identity.cognitoIdentityId",
    "cognito-identity-pool-id" : "$context.identity.cognitoIdentityPoolId",
    "http-method" : "$context.httpMethod",
    "stage" : "$context.stage",
    "source-ip" : "$context.identity.sourceIp",
    "user" : "$context.identity.user",
    "user-agent" : "$context.identity.userAgent",
    "user-arn" : "$context.identity.userArn",
    "request-id" : "$context.requestId",
    "resource-id" : "$context.resourceId",
    "resource-path" : "$context.resourcePath"
  }
}
EOT
  }
}

resource "aws_api_gateway_deployment" "guardian_deployment" {
  depends_on  = [aws_api_gateway_integration.guardian_integration]
  rest_api_id = aws_api_gateway_rest_api.guardian_api.id
}

resource "aws_api_gateway_stage" "api_stage" {
  deployment_id = aws_api_gateway_deployment.guardian_deployment.id
  rest_api_id   = aws_api_gateway_rest_api.guardian_api.id
  stage_name    = "dev"
  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_logs.arn
    format          = "$context.requestId $context.identity.sourceIp $context.httpMethod $context.resourcePath $context.status"
  }
}

resource "aws_api_gateway_account" "apigw_account" {
  cloudwatch_role_arn = aws_iam_role.apigw_iam_role.arn
}


resource "aws_api_gateway_method_settings" "api_method_settings" {
  rest_api_id = aws_api_gateway_rest_api.guardian_api.id
  stage_name  = aws_api_gateway_stage.api_stage.stage_name
  method_path = "*/*"

  settings {
    metrics_enabled = true
    logging_level   = "INFO"
  }
}

resource "aws_api_gateway_usage_plan" "guardian_usage_plan" {
  name        = "Daily"
  description = "50 API calls per day"

  quota_settings {
    limit  = 50
    period = "DAY"
  }
}
