#!/usr/bin/env python3
import os
import aws_cdk as cdk
from iac.portfolio_stack import PortfolioIacStack
from iac.certificate_stack import CertificateStack

app = cdk.App()

certificate_stack = CertificateStack(
    app,
    "CertificateStack",
    env=cdk.Environment(
        account=os.getenv('CDK_DEFAULT_ACCOUNT'),
        region='us-east-1'
    )
)

PortfolioIacStack(
    app,
    "PortfolioStack",
    certificate_stack = certificate_stack,
    env=cdk.Environment(
        account=os.getenv('CDK_DEFAULT_ACCOUNT'),
        region=os.getenv('CDK_DEFAULT_REGION')
    ),
    cross_region_references=True
)

app.synth()
