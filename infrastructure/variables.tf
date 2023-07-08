variable "domain_name" {
    default = "journalarticle.chat"
    type = string
}

variable "api_domain_name" {
    default = "api.journalarticle.chat"
    type = string
}

variable "bucket_name" {
    default = "journalarticle.chat"
    type = string
}

variable us-east-1-cert {
    default = "arn:aws:acm:us-east-1:637364745310:certificate/dc74b20b-8e46-4882-b50d-49dfe1864ee3"
    type = string
}

# variable "pgvector_password" {
#     type = string
#     sensitive = true
# }

# variable "namecheap_api_key" {
#     description = "Namecheap APIKey"
#     type = string
# }
