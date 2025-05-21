resource "yandex_storage_bucket" "this" {
  bucket         = var.bucket_name
  acl            = var.acl
  force_destroy  = false
  max_size       = 5368709120
}