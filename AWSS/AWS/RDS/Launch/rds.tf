# creating security group for RDS DB .

resource "aws_security_group" "VA2PT_RDS_SG" {
  name_prefix = "VA2PT-Rds-Sg"

  ingress {
    from_port = 3306
    to_port   = 3306
    protocol  = "tcp"             # type of protocol
    cidr_blocks = ["10.0.0.0/8"]
  }
}

# Creating RDB data base in aws console 

resource "aws_db_instance" "VA2PT_RDS_DB" {
  engine               = var.rds_db_engine
  engine_version       = var.rds_db_engine_version
  instance_class       = var.rds_db_instance_class
  allocated_storage    = var.rds_db_allocated_storage
  storage_type         = var.rdb_db_storage_type
  db_name               = var.rds_db_name
  username             = var.rds_db_username
  password             = var.rds_db_password
  subnet_group_name    = "VA2PT-db-Subnet-Group"
  vpc_security_group_ids = [aws_security_group.VA2PT_RDS_SG.id]

  tags = {
    Name = "VA2PT-RDS"
  }
}