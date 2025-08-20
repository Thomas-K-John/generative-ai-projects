variable "region" {
  type        = string
  description = "AWS region for all resources."
  default     = "us-east-1"
}

variable "project_name" {
  type        = string
  description = "Name of the project."
  default     = "AWS Bedrock Code Generatior"
}

variable "s3_bucket_name" {
  type        = string
  description = "Name of the S3 bucket to store the generated code."
  default     = "code-generator-aws-bedrock"
}

