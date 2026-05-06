# SecureScale — AWS Cloud Infrastructure Overview

## What is SecureScale
SecureScale is a production-grade, multi-AZ AWS infrastructure project 
built entirely from scratch. It deploys in under 3 minutes using 
Terraform Infrastructure as Code.

## Architecture
- VPC with public and private subnets across us-east-1a and us-east-1b
- Application Load Balancer distributing traffic across both AZs
- EC2 instances running Apache in public subnets
- RDS MySQL database in private subnets with no public access
- S3 encrypted bucket for application assets
- CloudTrail audit logging all API calls
- CloudWatch monitoring with SNS alerting

## Auto Scaling
ASG desired=2, min=1, max=2. If an instance fails health checks ASG 
automatically launches a replacement. Apache installs via user data 
script on first boot — zero manual intervention required.

## Health Checks
ALB runs HTTP health checks every 30 seconds on port 80 at path /.
5 consecutive successes = healthy. 2 failures = unhealthy, pulled 
from rotation automatically.

## Security
- Security groups — EC2 only accepts traffic from ALB, not internet
- IAM least privilege — scoped terraform-user, EC2 role with minimum permissions
- Session Manager replaces SSH — no open port 22
- CloudTrail records every AWS API call

## Terraform
13 files covering VPC, security groups, ALB, ASG, RDS, S3, 
CloudTrail, monitoring, AI layer, and dashboard.
State stored in S3 with DynamoDB locking.

## CI/CD Pipeline
GitHub Actions — every push triggers terraform plan automatically.
Gated approval required before terraform apply touches AWS.

## AI Ops Advisor
Lambda function triggered every 6 hours by EventBridge.
Pulls CloudWatch metrics, sends to Amazon Bedrock Nova Lite for analysis.
Generates cost, performance, and security recommendations.
Stores report in S3 and emails via SNS.

## Health Assessment Results
Last AI analysis found CPU at 0.48% — healthy.
ALB latency at 0.0 seconds — excellent.
Zero unhealthy hosts. Zero 5XX errors.
Recommendation: rightsize instances due to low CPU utilization.
