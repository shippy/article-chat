resource "aws_route53_zone" "prod" {
    name = var.domain_name
    vpc {
      vpc_id     = aws_vpc.chat_vpc.id
      vpc_region = "eu-central-1"  # Replace with your desired region
    }

}

resource "aws_route53_record" "chat_r53_record" {
  zone_id = aws_route53_zone.prod.zone_id
  name    = var.domain_name
  type    = "A"

  alias {
    name                   = aws_cloudfront_distribution.chat_s3_distribution.domain_name
    zone_id                = aws_cloudfront_distribution.chat_s3_distribution.hosted_zone_id
    evaluate_target_health = false
  }
}

# resource "aws_route53_record" "chat_r53_nameservers" {
#   zone_id = aws_route53_zone.prod.zone_id
#   name    = var.domain_name
#   type    = "NS"
#   ttl     = "172800"  # 2 days

#   records = aws_route53_record.chat_r53_record.name_servers
# }


resource "aws_s3_bucket" "frontend" {
  bucket = var.bucket_name
}

resource "aws_s3_bucket_website_configuration" "frontend_config" {
  bucket = aws_s3_bucket.frontend.id
  index_document {
    suffix = "index.html"
  }
  error_document {
    key = "index.html"
  }
}

resource "aws_cloudfront_distribution" "chat_s3_distribution" {
  origin {
    domain_name = aws_s3_bucket.frontend.bucket_regional_domain_name
    origin_id   = var.bucket_name

    s3_origin_config {
      origin_access_identity = aws_cloudfront_origin_access_identity.chat_oai.cloudfront_access_identity_path
    }
  }

  enabled             = true
  is_ipv6_enabled     = true
  comment             = "Chat app distribution"
  default_root_object = "index.html"

  default_cache_behavior {
    allowed_methods  = ["DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT"]
    cached_methods   = ["GET", "HEAD"]
    target_origin_id = var.bucket_name

    forwarded_values {
      query_string = false

      cookies {
        forward = "none"
      }
    }

    viewer_protocol_policy = "redirect-to-https"
    min_ttl                = 0
    default_ttl            = 3600
    max_ttl                = 86400
  }

  price_class = "PriceClass_100"

  restrictions {
    geo_restriction {
      restriction_type = "none"
    }
  }

  # aliases = [var.domain_name]  # Requires additional steps to prepare certificate (need ACM)
  viewer_certificate {
    cloudfront_default_certificate = true
  }
}

resource "aws_cloudfront_origin_access_identity" "chat_oai" {
  comment = "OAI for chat app"
}

data "aws_iam_policy_document" "frontend_policy" {
  statement {
    sid     = "1"
    effect  = "Allow"
    actions = ["s3:GetObject"]
    resources = [
      "${aws_s3_bucket.frontend.arn}/*"
    ]

    principals {
      type        = "AWS"
      identifiers = [aws_cloudfront_origin_access_identity.chat_oai.iam_arn]
    }
  }
}

resource "aws_s3_bucket_policy" "frontend_policy" {
  bucket = aws_s3_bucket.frontend.id
  policy = data.aws_iam_policy_document.frontend_policy.json
}


# # Create the IAM policy for the S3 bucket access
# resource "aws_iam_policy" "access_frontend_bucket" {
#   name        = "access-frontend-bucket"
#   description = "Policy for accessing the Vue.js files S3 bucket"

#   policy = <<EOF
# {
#   "Version": "2012-10-17",
#   "Statement": [
#     {
#       "Effect": "Allow",
#       "Action": [
#         "s3:GetObject"
#       ],
#       "Resource": [
#         "arn:aws:s3:::${aws_s3_bucket.frontend.id}/*"
#       ]
#     }
#   ]
# }
# EOF
# }

# # Create the IAM role for the ELB
# resource "aws_iam_role" "elb_role" {
#   name = "chat-elb-role"
#   assume_role_policy = <<EOF
# {
#   "Version": "2012-10-17",
#   "Statement": [
#     {
#       "Effect": "Allow",
#       "Principal": {
#         "Service": "elasticloadbalancing.amazonaws.com"
#       },
#       "Action": "sts:AssumeRole"
#     }
#   ]
# }
# EOF
# }

# # Attach the IAM policy to the role
# resource "aws_iam_role_policy_attachment" "elb_attachment" {
#   role       = aws_iam_role.elb_role.name
#   policy_arn = aws_iam_policy.access_frontend_bucket.arn
# }

# # Create the Elastic Load Balancer (ELB)
# resource "aws_elb" "chat_elb" {
#   name            = "chat-elb"
#   security_groups = [aws_security_group.chat_sg.id]
#   subnets         = [aws_subnet.chat_subnet.id]
#   instances       = []
#   listener {
#     instance_port     = 80
#     instance_protocol = "HTTP"
#     lb_port           = 80
#     lb_protocol       = "HTTP"
#   }
#   health_check {
#     healthy_threshold   = 2
#     unhealthy_threshold = 2
#     timeout             = 3
#     target              = "HTTP:80/"
#     interval            = 30
#   }
# }

# output "elb_dns" {
#   value = aws_elb.chat_elb.dns_name
# }
