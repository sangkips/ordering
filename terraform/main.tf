
module "network" {
  source   = "./modules/network"
  az_count = "2"
}

module "security" {
  source   = "./modules/security"
  app_port = 80
  vpc_id   = module.network.vpc_id
}


module "remote_backend" {
  source              = "./modules/backend"
  bucket_name         = "terraform-state-backend"
  dynamodb_table_name = "terraform-state-lock-table"
}

module "s3" {
  source      = "./modules/s3_img"
  bucket_name = "ordering-tech-for-all"
}
