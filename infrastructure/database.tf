resource "aws_db_subnet_group" "pgvector_subnet" {
    name = "main"
    subnet_ids = [aws_subnet.chat_subnet.id, aws_subnet.chat_subnet2.id]
}

resource "aws_kms_key" "rds" {
    description = "KMS key for RDS"
}

resource "aws_db_instance" "pgvector" {
    allocated_storage = 10
    db_name = "article_chat"
    db_subnet_group_name = aws_db_subnet_group.pgvector_subnet.name
    engine = "postgres"
    engine_version = 15
    skip_final_snapshot = true  # allow deletion
    instance_class = "db.t3.micro"
    username = "pgvector"
    # Password is retrievable from the Secrets Manager
    # and the secret_arn is listed in the Terraform state file
    manage_master_user_password = true
    master_user_secret_kms_key_id = aws_kms_key.rds.key_id
    # password = var.pgvector_password
    # publicly_accessible = true
    port = 5432
    vpc_security_group_ids = [aws_security_group.chat_sg.id]
}

output "db_url" {
    value = aws_db_instance.pgvector.address
}