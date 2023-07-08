# Must import manually created us-east-1 certificate so that it works with Cloudfront

# provider "aws" {
#     alias = "america"
#     region = "us-east-1"
# }

# import {
#     provider = aws.america
#     to = aws_acm_certificate.us-east-1-cert
#     id = "arn:aws:acm:us-east-1:637364745310:certificate/dc74b20b-8e46-4882-b50d-49dfe1864ee3"
# }

# resource "aws_acm_certificate" "us-east-1-cert" {
#     domain_name = var.domain_name
#     subject_alternative_names = [var.api_domain_name]
#     validation_method = "DNS"
#     tags = {
#         Name = "ArticleChat"
#     }
#     lifecycle {
#         create_before_destroy = true
#     }
# }