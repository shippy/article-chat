# Pursuant to website.tf
module "cognito_mailer" {
  source  = "voquis/ses-validated-domain-and-emails/aws"
  version = "0.0.1"
  zone_id = aws_route53_zone.prod.zone_id
  domain  = aws_route53_zone.prod.name
}
