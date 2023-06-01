# Create a EC2 security group

resource "aws_security_group" "VA2PT_EC2_SG" {
  name_prefix = "VA2PT-Ec2-Sg"

  ingress {
    from_port = 22
    to_port   = 22
    protocol  = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Resource block for EC2 instance

resource "aws_instance" "VA2PT" {
  ami           = var.ec2_ami                        # replace with your desired AMI ID
  instance_type = var.ec2_instance_type              # replace with your desired instance type

  tags = {
    Name = "va2pt"
  }

  # Replace with your desired subnet ID, security group IDs

  subnet_id              = aws_subnet.VA2PT_SUBNET_PVT.id
  vpc_security_group_ids = [aws_security_group.VA2PT_SG.id]
  

 }