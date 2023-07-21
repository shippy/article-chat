variable "aws_region" {
    default = "eu-central-1"
    type = string
}

variable "domain_name" {
    default = "journalarticle.chat"
    type = string
}

variable "api_domain_name" {
    default = "api.journalarticle.chat"
    type = string
}

variable "auth_domain_name" {
    default = "auth.journalarticle.chat"
    type = string
}

variable "bucket_name" {
    default = "journalarticle.chat"
    type = string
}

variable us-east-1-cert {
    default = "arn:aws:acm:us-east-1:637364745310:certificate/975283c5-0e0b-4088-9978-fb4fda71ff0e"
    type = string
}

data "aws_ssm_parameter" "openai_key" {
    name = "/articlechat/openai_key"
}

# variable "pgvector_password" {
#     type = string
#     sensitive = true
# }

# variable "namecheap_api_key" {
#     description = "Namecheap APIKey"
#     type = string
# }
