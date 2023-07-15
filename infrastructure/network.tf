# Create the VPC for the use case
resource "aws_vpc" "chat_vpc" {
  cidr_block = "10.0.0.0/16"  # Replace with your desired CIDR block
  tags = {
    Name = "chat-vpc"
  }
}

resource "aws_internet_gateway" "chat_igw" {
  vpc_id = aws_vpc.chat_vpc.id
}


# Create a security group for the ELB
resource "aws_security_group" "chat_sg" {
  name        = "chat-elb-sg"
  description = "Security group for the ELB"
  vpc_id      = aws_vpc.chat_vpc.id

  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Create a subnet for the ELB
resource "aws_subnet" "chat_subnet" {
  vpc_id            = aws_vpc.chat_vpc.id
  availability_zone = "eu-central-1a"
  cidr_block        = "10.0.3.0/24"
}

resource "aws_subnet" "chat_subnet2" {
  vpc_id            = aws_vpc.chat_vpc.id
  availability_zone = "eu-central-1b"
  cidr_block        = "10.0.4.0/24"
}

resource "aws_subnet" "chat_public_subnet_1" {
  vpc_id            = aws_vpc.chat_vpc.id
  availability_zone = "eu-central-1a"
  cidr_block        = "172.0.1.0/24"
}

resource "aws_subnet" "chat_public_subnet_2" {
  vpc_id            = aws_vpc.chat_vpc.id
  availability_zone = "eu-central-1b"
  cidr_block        = "172.0.2.0/24"
}