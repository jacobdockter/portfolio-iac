#!/usr/bin/env python3
import os
import aws_cdk as cdk
from iac.portfolio_stack import PortfolioIacStack
from iac.certificate_stack import CertificateStack
from iac.secret_stack import SecretStack

app = cdk.App()

secret_stack = SecretStack(
    app,
    "SecretStack",
    env=cdk.Environment(
        account=os.getenv('CDK_DEFAULT_ACCOUNT'),
        region=os.getenv('CDK_DEFAULT_REGION')
    )
)

certificate_stack = CertificateStack(
    app,
    "CertificateStack",
    secret_stack=secret_stack,
    env=cdk.Environment(
        account=os.getenv('CDK_DEFAULT_ACCOUNT'),
        region='us-east-1'
    ),
    cross_region_references=True
)

PortfolioIacStack(
    app,
    "PortfolioStack",
    certificate_stack = certificate_stack,
    secret_stack=secret_stack,
    env=cdk.Environment(
        account=os.getenv('CDK_DEFAULT_ACCOUNT'),
        region=os.getenv('CDK_DEFAULT_REGION')
    ),
    cross_region_references=True
)

app.synth()
