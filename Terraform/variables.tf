
variable "token" {
  description = "IAM token для Yandex Cloud"
  type        = string
}

variable "zone" {
  description = "Зона доступности"
  type        = string
  default     = "ru-central1-b"
}

# Основные переменные для провайдера
variable "service_account_key_file" {
  description = "Path to Yandex Cloud service account key file"
  type        = string
  sensitive   = true
}

variable "cloud_id" {
  description = "Yandex Cloud ID"
  type        = string
  sensitive   = true
}

variable "folder_id" {
  description = "Yandex Cloud Folder ID"
  type        = string
  sensitive   = true
}

# Переменные для S3 модуля
variable "bucket_name" {
  description = "Unique S3 bucket name"
  type        = string
  default     = null
}

variable "bucket_acl" {
  description = "Bucket ACL (private/public-read/etc)"
  type        = string
  default     = "private"
}

