# resource "aws_db_subnet_group" "pgvector_subnet" {
#     name = "main"
#     subnet_ids = [aws_subnet.chat_subnet.id, aws_subnet.chat_subnet2.id]
# }

# # resource "aws_kms_key" "pgvector" {
# #   description = "ArticleChat RDS KMS Key"
# # }

# resource "aws_db_instance" "pgvector" {
#     allocated_storage = 10
#     db_name = "article_chat"
#     db_subnet_group_name = aws_db_subnet_group.pgvector_subnet.name
#     engine = "postgres"
#     engine_version = 15
#    # skip_final_snapshot = true  # allow deletion
#     instance_class = "db.t3.micro"
#     username = "pgvector"
#     # manage_master_user_password = true
#     # master_user_secret_kms_key_id = aws_kms_key.pgvector.key_id
#     password = var.pgvector_password
#     # publicly_accessible = true
#     port = 5432
#     vpc_security_group_ids = [aws_security_group.chat_sg.id]
# }
