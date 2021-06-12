terraform {
    required_providers {
        aws = {
            source = "hashicorp/aws"
        }
    }
    backend "remote" {
    hostname = "app.terraform.io"
    organization = "feedback-engineering"

    workspaces {
      name = "pollinate"
    }
  }
}



provider "aws" {
    region = var.region
}

provider "kubernetes" {
  host                   = data.aws_eks_cluster.cluster.endpoint
  token                  = data.aws_eks_cluster_auth.cluster.token
  cluster_ca_certificate = base64decode(data.aws_eks_cluster.cluster.certificate_authority.0.data)
}

data "aws_availability_zones" "available" {
}

data "aws_eks_cluster" "cluster" {
  name = module.eks.cluster_id
}

data "aws_eks_cluster_auth" "cluster" {
  name = module.eks.cluster_id
}

locals {
  cluster_name = "test-eks-pollinate"
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 2.47"

  name                 = "test-vpc"
  cidr                 = "10.0.0.0/16"
  azs                  = data.aws_availability_zones.available.names
  private_subnets      = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
  public_subnets       = ["10.0.4.0/24", "10.0.5.0/24", "10.0.6.0/24"]
  enable_nat_gateway   = true
  single_nat_gateway   = true
  enable_dns_hostnames = true

  public_subnet_tags = {
    "kubernetes.io/cluster/${local.cluster_name}" = "shared"
    "kubernetes.io/role/elb"                      = "1"
  }

  private_subnet_tags = {
    "kubernetes.io/cluster/${local.cluster_name}" = "shared"
    "kubernetes.io/role/internal-elb"             = "1"
  }
}




module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "17.1.0"
  cluster_name = "test-cluster"
  vpc_id = module.vpc.vpc_id
  subnets = module.vpc.private_subnets
  cluster_version = "1.17"

  worker_groups = [
      {
          name          = "worker-group-1"
          instance_size = "t3.micro"
          asg_max_size  = var.max_cluster_size
      }
  ]

}

resource "aws_dynamodb_table" "connections" {
    name            = "connections"
    billing_mode    = "PAY_PER_REQUEST"
    hash_key        = "nodeID"
    range_key        = "connectionTime"

    attribute {
        name = "nodeID"
        type = "S"
    }

    attribute {
        name = "connectionTime"
        type = "S"
    }
}




