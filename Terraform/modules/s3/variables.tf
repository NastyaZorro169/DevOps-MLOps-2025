variable "bucket_name" {
  description = "Bucket name"
  type        = string
}

variable "acl" {
  description = "ACL setting"
  type        = string
  default     = "private"
}

variable "folder_id" {
  description = "Folder ID in Yandex Cloud"
  type        = string
}