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
}

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