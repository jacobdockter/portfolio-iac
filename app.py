#!/usr/bin/env python3
import aws_cdk as cdk
from iac.portfolio_stack import PortfolioIacStack
from iac.certificate_stack import CertificateStack
from iac.constants import (
    RESOURCE_NAME,
    AWS_ACCOUNT_ID,
    AWS_REGION
)

app = cdk.App()

certificate_stack = CertificateStack(
    app,
    "CertificateStack",
    env=cdk.Environment(
        account=AWS_ACCOUNT_ID,
        region='us-east-1'
    )
)

PortfolioIacStack(
    app,
    "PortfolioStack",
    resource_name=RESOURCE_NAME,
    certificate_stack = certificate_stack,
    env=cdk.Environment(
        account=AWS_ACCOUNT_ID,
        region=AWS_REGION
    ),
    cross_region_references=True
)

app.synth()
