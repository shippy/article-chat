resource "aws_cognito_user_pool" "main" {
  name = "article_chat_user_pool"

  password_policy {
    minimum_length    = 12
    require_lowercase = true
    require_numbers   = true
    require_symbols   = true
    require_uppercase = true
    temporary_password_validity_days = 7
  }

  username_attributes = ["email"]
  auto_verified_attributes = ["email"]
  username_configuration {
    case_sensitive = false
  }

  admin_create_user_config {
    allow_admin_create_user_only = true
  }
}

resource "aws_cognito_user_pool_client" "client" {
  name = "article_chat_user_pool_client"

  user_pool_id = aws_cognito_user_pool.main.id

  allowed_oauth_flows_user_pool_client = true
  allowed_oauth_flows = ["code", "implicit"]
  allowed_oauth_scopes = ["email", "openid"]
  # Important - nothing works without it:
  supported_identity_providers = ["COGNITO"]


  callback_urls = [
    "https://${var.api_domain_name}/callback",
    "https://${var.api_domain_name}/redirect",
    "http://localhost/callback",
    "http://localhost/redirect"
  ]
  default_redirect_uri  = "https://${var.api_domain_name}/redirect"
  logout_urls = ["https://${var.api_domain_name}/logout"]
  
  generate_secret = true
}

resource "aws_cognito_user_pool_domain" "main" {
  domain          = var.auth_domain_name
  certificate_arn = var.us-east-1-cert
  user_pool_id    = aws_cognito_user_pool.main.id
}

resource "aws_route53_record" "auth-cognito-A" {
  name    = var.auth_domain_name
  # equivalent to aws_cognito_user_pool_domain.main.domain
  type    = "A"
  zone_id = aws_route53_zone.prod.zone_id
  alias {
    evaluate_target_health = false

    name    = aws_cognito_user_pool_domain.main.cloudfront_distribution
    zone_id = aws_cognito_user_pool_domain.main.cloudfront_distribution_zone_id
  }
}

## Outputs

output "user_pool_id" {
  value = aws_cognito_user_pool.main.id
}

output "user_pool_domain" {
  value = aws_cognito_user_pool_domain.main.domain
}

output "user_pool_secret" {
  value = aws_cognito_user_pool_client.client.client_secret
  sensitive = true
}

