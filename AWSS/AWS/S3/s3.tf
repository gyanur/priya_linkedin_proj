# creating S3 bucket

resource "aws_s3_bucket" "my_bucket" {
  bucket = "va2pt-s3-bucket" // change this to your preferred bucket name
  tags = {
    Name = "va2pt S3 Bucket"
  }
}