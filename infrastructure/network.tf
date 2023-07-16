# Create the VPC for the use case
resource "aws_vpc" "chat_vpc" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name = "chat-vpc"
  }
}

resource "aws_internet_gateway" "chat_igw" {
  vpc_id = aws_vpc.chat_vpc.id
}


# Elastic-IP (eip) for NAT
resource "aws_eip" "nat_eip" {
  vpc        = true
  depends_on = [aws_internet_gateway.chat_igw]
}

# NAT
resource "aws_nat_gateway" "nat" {
  allocation_id = aws_eip.nat_eip.id
  subnet_id     = aws_subnet.chat_public_subnet_1.id

  tags = {
    Name        = "article-chat-nat"
  }
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
  cidr_block        = "10.0.20.0/24"
  map_public_ip_on_launch = true
  tags = {
    Name = "chat-public-subnet-1"
  }
}

resource "aws_subnet" "chat_public_subnet_2" {
  vpc_id            = aws_vpc.chat_vpc.id
  availability_zone = "eu-central-1b"
  cidr_block        = "10.0.21.0/24"
  map_public_ip_on_launch = true
  tags = {
    Name = "chat-public-subnet-2"
  }
}

# Route tables
# Public Route Table
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.chat_vpc.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.chat_igw.id
  }

  tags = {
    Name = "chat-public-rt"
  }
}

# Associate the public route table with the public subnets
resource "aws_route_table_association" "public_1" {
  subnet_id      = aws_subnet.chat_public_subnet_1.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "public_2" {
  subnet_id      = aws_subnet.chat_public_subnet_2.id
  route_table_id = aws_route_table.public.id
}

# Private Route Table
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.chat_vpc.id

  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.nat.id
  }

  tags = {
    Name = "chat-private-rt"
  }
}

# Associate the private route table with the private subnets
resource "aws_route_table_association" "private_1" {
  subnet_id      = aws_subnet.chat_subnet.id
  route_table_id = aws_route_table.private.id
}

resource "aws_route_table_association" "private_2" {
  subnet_id      = aws_subnet.chat_subnet2.id
  route_table_id = aws_route_table.private.id
}

