
provider "aws" {
}

resource "aws_s3_bucket" "s3_bucket" {
  bucket = var.s3_bucket_name
}

# IAM role that allows AWS Lambda to assume permissions
resource "aws_iam_role" "lambda_role" {
  name               = "aws_bedrock_lambda_role"
  assume_role_policy = file("${path.module}/policies/lambda_policy.json")
}

# IAM policy to allow Lambda to write logs to CloudWatch
resource "aws_iam_policy" "iam_policy_for_lambda" {

  name        = "aws_iam_policy_for_lambda_role"
  path        = "/"
  description = "AWS IAM Policy for managing aws lambda role"
  policy      = file("${path.module}/policies/iam_policy_for_lambda.json")
}

# Attach logging policy to Lambda execution role
resource "aws_iam_role_policy_attachment" "iam_policy_to_lambda_role" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.iam_policy_for_lambda.arn
}

resource "aws_iam_role_policy_attachment" "bedrock_access_to_lambda_role" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonBedrockFullAccess"
}

resource "aws_iam_role_policy_attachment" "s3_access_to_lambda_role" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

# Archive the Lambda function into a ZIP file.
resource "archive_file" "zip_lambda_function" {
  type        = "zip"
  source_dir  = "${path.module}/lambda_function/"
  output_path = "${path.module}/build/code_generator.zip"
}

# Create a lambda function
resource "aws_lambda_function" "lambda_function" {
  filename         = "${path.module}/build/code_generator.zip"
  function_name    = "code_generator"
  role             = aws_iam_role.lambda_role.arn
  handler          = "code_generator.lambda_handler"
  runtime          = "python3.12"
  timeout          = 120
  source_code_hash = filebase64sha256("${path.module}/build/code_generator.zip")
  depends_on       = [aws_iam_role_policy_attachment.iam_policy_to_lambda_role, aws_iam_role_policy_attachment.bedrock_access_to_lambda_role, aws_iam_role_policy_attachment.s3_access_to_lambda_role]
}

# Create API Gateway
resource "aws_api_gateway_rest_api" "api_gateway" {
  name        = "code_generator_api"
  description = "API for code generation"

  endpoint_configuration {
    types = ["REGIONAL"]
  }
}

resource "aws_api_gateway_resource" "api_gateway_resource" {
  parent_id   = aws_api_gateway_rest_api.api_gateway.root_resource_id
  path_part   = "code_generator"
  rest_api_id = aws_api_gateway_rest_api.api_gateway.id
}

resource "aws_api_gateway_method" "api_gateway_method" {
  resource_id   = aws_api_gateway_resource.api_gateway_resource.id
  rest_api_id   = aws_api_gateway_rest_api.api_gateway.id
  http_method   = "POST"
  authorization = "NONE"
  request_parameters = {
    "method.request.querystring.prompt" = true
  }
}

resource "aws_api_gateway_integration" "lambda_integration" {
  http_method             = aws_api_gateway_method.api_gateway_method.http_method
  resource_id             = aws_api_gateway_resource.api_gateway_resource.id
  rest_api_id             = aws_api_gateway_rest_api.api_gateway.id
  integration_http_method = "POST"
  type                    = "AWS"
  uri                     = aws_lambda_function.lambda_function.invoke_arn
  #   request_templates = {
  #     "application/json" = <<EOF
  # {
  #   "prompt": "$util.escapeJavaScript($input.params('prompt'))"
  # }
  # EOF
  #   }
  passthrough_behavior = "WHEN_NO_TEMPLATES"
  content_handling     = "CONVERT_TO_TEXT"
}

resource "aws_lambda_permission" "apigw_lambda_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_function.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.api_gateway.execution_arn}/*/POST/code_generator"
}

resource "aws_api_gateway_deployment" "api_gateway_deployment" {
  rest_api_id = aws_api_gateway_rest_api.api_gateway.id
  triggers = {
    redeployment = sha1(jsonencode([
      aws_api_gateway_resource.api_gateway_resource.id,
      aws_api_gateway_method.api_gateway_method.id,
      aws_api_gateway_integration.lambda_integration.id
    ]))
  }
  lifecycle {
    create_before_destroy = true
  }
  depends_on = [
    aws_api_gateway_integration.lambda_integration
  ]
}

resource "aws_api_gateway_stage" "api_stage" {
  deployment_id = aws_api_gateway_deployment.api_gateway_deployment.id
  rest_api_id   = aws_api_gateway_rest_api.api_gateway.id
  stage_name    = "prod"
}

resource "aws_api_gateway_method_response" "api_method_response_200" {
  rest_api_id = aws_api_gateway_rest_api.api_gateway.id
  resource_id = aws_api_gateway_resource.api_gateway_resource.id
  http_method = aws_api_gateway_method.api_gateway_method.http_method
  status_code = "200"
  response_models = {
    "application/json" = "Empty"
  }
}

resource "aws_api_gateway_integration_response" "integration_response_200" {
  rest_api_id = aws_api_gateway_rest_api.api_gateway.id
  resource_id = aws_api_gateway_resource.api_gateway_resource.id
  http_method = aws_api_gateway_method.api_gateway_method.http_method
  status_code = "200"
  response_templates = {
    "application/json" = ""
  }
  selection_pattern = ""
  depends_on        = [aws_api_gateway_integration.lambda_integration]
}

