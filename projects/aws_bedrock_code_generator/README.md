# Project 2: AWS AI Code Generator with Bedrock, Lambda, API Gateway, S3, and Terraform

![View the architecture diagram](https://github.com/Thomas-K-John/generative-ai-projects/blob/main/projects/aws_bedrock_code_generator/data/architecture.jpg)

## Summary

- This project demonstrates a serverless AI-powered code generation service using Amazon Bedrock (Titan model) integrated with AWS Lambda and exposed via API Gateway.
- The system allows users to send natural language programming instructions and receive ready-to-use source code in their preferred programming language.
- Generated code is automatically stored in Amazon S3 for later retrieval.
- Terraform is used for full infrastructure provisioning.

## Key elements include:

- Amazon API Gateway – Provides a REST API endpoint for external requests.
- AWS Lambda – Executes the code_generator.py script to process inputs.
- Amazon Bedrock – Powers the generative AI functionality using amazon.titan-text-premier-v1:0.
- Amazon S3 – Stores generated code files with proper extensions (.py, .java, .js, .sql, etc.).
- Terraform – Automates provisioning of S3, Lambda, IAM roles, and API Gateway resources.

## Prerequisites

1. AWS Account with permissions for Lambda, S3, API Gateway, and Bedrock.
2. Terraform installed locally.
3. AWS CLI configured with credentials.
4. AWS S3 bucket for Terraform remote state.

## Tips:

1. Deploying Infrastructure with Terraform
   
   Initialize Terraform:
   ```terraform init -backend-config="backend_aws_bedrock_code_generator.hcl"```

   Apply configuration:
   `terraform apply`
   
2. Make a POST request to the API Gateway endpoint
   * Send Request for powershell users:-   
   ``` curl -Method POST `  -Uri "<API_GATEWAY_ENDPOINT>" -Headers @{ "Content-Type" = "application/json" } `-Body "{""message"": ""Write a function to reverse a string"", ""language"": ""python""}" ```
   
   * Send Request for linux users:-
   ```curl -X POST "<API_GATEWAY_ENDPOINT>" -H "Content-Type: application/json" -d '{"message":"Write a function to reverse a string","language":"python"}' ```

   * Response
   ```{"statusCode": 200,"body": "\"Code generation Complete\""}```

   * Output
   Generated code is saved to:
   ```s3://code-generator-aws-bedrock/code-output/<timestamp>.py```
