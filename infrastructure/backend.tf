# Following tutorial at https://radix.ai/blog/2020/12/swiftly-writing-and-deploying-apis-to-stay-agile/
resource "aws_ecr_repository" "main" {
  name = "article-chat"
}

output "repository_url" {
  value = aws_ecr_repository.main.repository_url
}

resource "aws_ecs_cluster" "main" {
  name = "article-chat"
}


module "alb" {
  source  = "terraform-aws-modules/alb/aws"
  version = "~> 5.0"

  name            = "article-chat-alb"
  vpc_id          = aws_vpc.chat_vpc.id
  subnets         = [aws_subnet.chat_public_subnet_1.id, aws_subnet.chat_public_subnet_2.id]
  # subnets         = [aws_subnet.chat_subnet.id, aws_subnet.chat_subnet2.id]
  security_groups = [aws_security_group.chat_sg.id]

  target_groups = [
    {
      name         = "article-chat-tg"
      backend_port         = 80
      backend_protocol     = "HTTP"
      target_type  = "ip"
      vpc_id       = aws_vpc.chat_vpc.id
      health_check = {
        path    = "/docs"
        port    = "80"
        matcher = "200-399"
      }
    }
  ]

  # http_tcp_listeners = [
  #   {
  #     port               = 80
  #     protocol           = "HTTP"
  #     target_group_index = 0
  #   }
  # ]
  http_tcp_listeners = [
    {
      port        = 80
      protocol    = "HTTP"
      action_type = "redirect"
      redirect = {
        port        = "443"
        protocol    = "HTTPS"
        status_code = "HTTP_301"
      }
    }
  ]

  https_listeners = [
    {
      port               = 443
      protocol           = "HTTPS"
      certificate_arn    = aws_acm_certificate.domain_certificate_request.arn
      target_group_index = 0
    }
  ]

}

module "container_definition" {
  source = "git::https://github.com/cloudposse/terraform-aws-ecs-container-definition.git?ref=tags/0.60.0"

  container_name  = "article-chat-container"
  container_image = aws_ecr_repository.main.repository_url
  port_mappings   = [
    {
      containerPort = 80
      hostPort      = 80
      protocol      = "tcp"
    }
  ]
  log_configuration = {
    logDriver = "awslogs"
    options = {
      awslogs-group         = aws_cloudwatch_log_group.ecs_logs.name
      awslogs-region        = var.aws_region
      awslogs-stream-prefix = "ecs"
    }
  }
  environment = [
    {
      name  = "DEPLOYMENT_DOMAIN"
      value = var.api_domain_name
    },
    {
      name  = "FRONTEND_DOMAIN"
      value = "https://${var.domain_name}"
    },
    {
      name  = "COGNITO_REGION"
      value = var.aws_region
    },
    {
      name  = "COGNITO_POOL_ID"
      value = aws_cognito_user_pool.main.id
    },
    {
      name  = "COGNITO_APP_CLIENT_ID"
      value = aws_cognito_user_pool_client.client.id
    },
    {
      name  = "COGNITO_REDIRECT_URL"
      value = "https://${var.api_domain_name}/auth/callback"
    },
    {
      name  = "COGNITO_DOMAIN",
      value = var.auth_domain_name
    },
    {
      name  = "POSTGRES_URL",
      value = aws_db_instance.pgvector.address
    },
    {
      name  = "POSTGRES_PORT",
      value = aws_db_instance.pgvector.port
    },
    {
      name = "POSTGRES_USER",
      value = aws_db_instance.pgvector.username
    },
    {
      name  = "POSTGRES_DB",
      value = aws_db_instance.pgvector.db_name
    }
    # Password passed in as a secret below in PGVECTOR_CREDENTIALS
  ]
  secrets = [
    {
      name      = "COGNITO_CLIENT_SECRET"
      valueFrom = aws_ssm_parameter.cognito_client_secret.arn
    },
    {
      name      = "POSTGRES_PASSWORD"
      valueFrom = aws_ssm_parameter.pgvector_password.arn
    },
    {
      name      = "OPENAI_API_KEY"
      valueFrom = data.aws_ssm_parameter.openai_key.arn
    }
  ]
}

resource "aws_cloudwatch_log_group" "ecs_logs" {
  name = "/ecs/article-chat"
}

# # Permit the above task to actually retrieve the secrets
# resource "aws_iam_policy" "ecs_secrets" {
#   name        = "ecs_secrets"
#   description = "Allows ECS tasks to retrieve secrets from Secrets Manager"
#   policy      = <<EOF
# {
#   "Version": "2012-10-17",
#   "Statement": [
#     {
#       "Action": [
#         "secretsmanager:GetSecretValue"
#       ],
#       "Resource": [
#         "${aws_secretsmanager_secret.cognito_client_secret.arn}",
#         "${aws_db_instance.pgvector.master_user_secret[0].secret_arn}"
#       ],
#       "Effect": "Allow"
#     }
#   ]
# }
# EOF
# }

# # FIXME: This doesn't work because the module doesn't export the execution role ARN
# resource "aws_iam_role_policy_attachment" "ecs_secrets_attachment" {
#   role       = module.ecs_alb_service_task.execution_role_arn  // Replace with actual output variable
#   policy_arn = aws_iam_policy.ecs_secrets.arn
# }

# Finally, define an automatic load balancer (ALB) for the task

module "ecs_alb_service_task" {
  source = "git::https://github.com/cloudposse/terraform-aws-ecs-alb-service-task.git?ref=tags/0.70.0"

  namespace                 = "rdx"
  stage                     = "prod"
  name                      = "article-chat"
  container_definition_json = module.container_definition.json_map_encoded_list
  ecs_cluster_arn           = aws_ecs_cluster.main.arn
  launch_type               = "FARGATE"
  vpc_id                    = aws_vpc.chat_vpc.id
  security_group_ids        = [aws_security_group.chat_sg.id]
  # subnet_ids                = [aws_subnet.chat_public_subnet_1.id, aws_subnet.chat_public_subnet_2.id]
  subnet_ids                = [aws_subnet.chat_subnet.id, aws_subnet.chat_subnet2.id]

  health_check_grace_period_seconds  = 60
  ignore_changes_task_definition     = false

  ecs_load_balancers = [
    {
      target_group_arn = module.alb.target_group_arns[0]
      elb_name         = ""
      container_name   = "article-chat-container"
      container_port   = 80
  }]
}

resource "aws_route53_record" "api-backend-A" {
  zone_id = aws_route53_zone.prod.zone_id
  name    = var.api_domain_name
  type    = "A"

  alias {
    name                   = module.alb.this_lb_dns_name
    zone_id                = module.alb.this_lb_zone_id

    evaluate_target_health = true
  }
}