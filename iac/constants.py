"""constants.py
Defines constants for the portfolio suite of applications
"""
import os

AWS_REGION = os.getenv("CDK_DEFAULT_ACCOUNT", "us-west-2")
AWS_ACCOUNT_ID = os.getenv("CDK_DEFAULT_ACCOUNT", None)
VOICE_CLIENT_REPOSITORY = "voice-portfolio-client"
DEV_CLIENT_REPOSITORY = "dev-portfolio-client"
DIRECTORY_CLIENT_REPOSITORY = "directory-portfolio-client"
IAC_REPOSITORY = "portfolio-iac"
GITHUB_ACCOUNT = "jacobdockter"
RESOURCE_NAME = "dockter"
CODESTAR_ARN = f"arn:aws:codestar-connections:{AWS_REGION}:{AWS_ACCOUNT_ID}:connection/eff81f9d-3087-4f5a-b273-89f91ca7be75"
BASE_DOMAIN_NAME = "jacobdockter.com"
DOMAIN_ZONE_ID = "Z01560252SHMW5HXWHV6L"
