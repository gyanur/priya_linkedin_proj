# Creating a virtual private cloud (VPC)

resource "aws_vpc" "VA2PT_VPC" {
  cidr_block = var.vpc_cidr_block
}

# Creating a public subnet 

resource "aws_subnet" "VA2PT_SUBNET_PBLC" {
  vpc_id     = aws_vpc.VA2PT_VPC.id
  cidr_block = var.vpc_public_subnet_cidr_block

  tags = {
    Name = "VA2PT-Public-Subnet"
  }
}

# Creating a private subnet 

resource "aws_subnet" "VA2PT_SUBNET_PVT" {
  vpc_id     = aws_vpc.VA2PT_VPC.id
  cidr_block = var.vpc_private_subnet_cidr_block

  tags = {
    Name = "VA2PT-Private-Subnet"
  }
}