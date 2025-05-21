
terraform {
  required_providers {
    yandex = {
      source  = "yandex-cloud/yandex"
      version = "~> 0.90"
    }
  }
}

provider "yandex" {
  service_account_key_file = var.service_account_key_file
  cloud_id  = var.cloud_id
  folder_id = var.folder_id
  zone      = var.zone
}

resource "random_id" "bucket_suffix" {
  byte_length = 4
}

resource "yandex_vpc_network" "default" {
  name = "default-network"
}

resource "yandex_vpc_subnet" "default" {
  name           = "default-subnet"
  zone           = var.zone
  network_id     = yandex_vpc_network.default.id
  v4_cidr_blocks = ["10.0.0.0/24"]
}

module "s3_bucket" {
  source      = "./modules/s3"
  bucket_name = coalesce(var.bucket_name, "bucket-${random_id.bucket_suffix.hex}")
  acl         = var.bucket_acl
  folder_id   = var.folder_id
}

data "yandex_compute_image" "ubuntu" {
  family = "ubuntu-2204-lts"
}

data "template_file" "cloud_init" {
  template = file("${path.module}/cloud-init.tpl.yaml")
  vars = {
    bucket_name = module.s3_bucket.bucket_id
  }
}

resource "yandex_compute_instance" "vm" {
  name        = "s3-client-vm"
  platform_id = "standard-v1"
  zone        = "ru-central1-b"

  resources {
    cores  = 2
    memory = 2
  }

  boot_disk {
    initialize_params {
      image_id = data.yandex_compute_image.ubuntu.id
    }
  }

  network_interface {
    subnet_id = yandex_vpc_subnet.default.id
    nat       = true
  }

  metadata = {
    user-data = data.template_file.cloud_init.rendered
  }
}
