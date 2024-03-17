# Create the user for Github Actions

resource "aws_iam_user" "github_actions_user" {
  name = "article-chat-gha-user"
}

resource "aws_iam_access_key" "gh_access_key" {
  user = aws_iam_user.github_actions_user.name
}

output "gh_secret_key" {
  value     = aws_iam_access_key.gh_access_key.secret
  sensitive = true
}

output "gh_access_key" {
  value = aws_iam_access_key.gh_access_key.id
}

data "aws_iam_policy_document" "gh_action_policy_doc" {
  statement {
    effect = "Allow"

    actions = [
      "s3:*",
    ]

    resources = [
      "${aws_s3_bucket.frontend.arn}",
      "${aws_s3_bucket.frontend.arn}/*"
    ]
  }

  statement {
    effect = "Allow"

    actions = [
      "cloudfront:CreateInvalidation",
    ]

    resources = [
      "arn:aws:cloudfront::*:distribution/${aws_cloudfront_distribution.chat_s3_distribution.id}"
    ]
  }

  # statement {
  #   effect = "Allow"

  #   actions = [
  #     "ecr:GetDownloadUrlForLayer",
  #     "ecr:BatchGetImage",
  #     "ecr:BatchCheckLayerAvailability",
  #     "ecr:PutImage",
  #     "ecr:InitiateLayerUpload",
  #     "ecr:UploadLayerPart",
  #     "ecr:CompleteLayerUpload",
  #   ]

  #   resources = [
  #     "${aws_ecr_repository.main.arn}"
  #   ]
  # }

  statement {
    effect = "Allow"
    actions = [
      "ecr:GetAuthorizationToken"
    ]
    resources = ["*"]
  }

  # # Allow forcing new deployment
  # statement {
  #   sid = "ForceNewDeployment"
  #   effect = "Allow"
  #   actions = [
  #     "ecs:UpdateService",
  #   ]
  #   resources = [
  #     "${module.ecs_alb_service_task.service_arn}"
  #   ]
  # }


  # Reload ALB
  statement {
    sid = "ForceALBReload"
    effect = "Allow"
    actions = [
      "elasticloadbalancing:DeregisterInstancesFromLoadBalancer",
      "elasticloadbalancing:RegisterInstancesWithLoadBalancer",
      "ec2:DescribeInstances"   
    ]
    resources = [
      "*"
    ]
  }

}

resource "aws_iam_policy" "gh_action_policy" {
  name        = "github_actions_policy"
  description = "Policy for GitHub Actions"
  policy      = data.aws_iam_policy_document.gh_action_policy_doc.json
}

resource "aws_iam_user_policy_attachment" "attach_policy" {
  user       = aws_iam_user.github_actions_user.name
  policy_arn = aws_iam_policy.gh_action_policy.arn
}

