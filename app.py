#!/usr/bin/env python3
import aws_cdk as cdk
from iac.portfolio_stack import PortfolioIacStack
from iac.certificate_stack import CertificateStack
from iac.secret_stack import SecretStack
from iac.constants import RESOURCE_NAME, AWS_ACCOUNT_ID, AWS_REGION

app = cdk.App()

secret_stack = SecretStack(
    app, "SecretStack", env=cdk.Environment(account=AWS_ACCOUNT_ID, region=AWS_REGION)
)

certificate_stack = CertificateStack(
    app,
    "CertificateStack",
    secret_stack=secret_stack,
    env=cdk.Environment(account=AWS_ACCOUNT_ID, region="us-east-1"),
    cross_region_references=True,
)

PortfolioIacStack(
    app,
    "PortfolioStack",
    resource_name=RESOURCE_NAME,
    certificate_stack=certificate_stack,
    env=cdk.Environment(account=AWS_ACCOUNT_ID, region=AWS_REGION),
    cross_region_references=True,
)

app.synth()
