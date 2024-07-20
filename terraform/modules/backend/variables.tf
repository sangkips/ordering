variable "bucket_name" {
  description = "Name of the S3 bucket"
  default     = "ordering-terraform-state-backend-990"
}

variable "dynamodb_table_name" {
  description = "Name of the DynamoDB table"
  default     = "ordering-db-terraform-state-lock"
}
