#!/usr/bin/env python3
import os
import aws_cdk as cdk
from iac.portfolio_stack import PortfolioStack

app = cdk.App()

PortfolioStack(
    app,
    "PortfolioStack",
    env=cdk.Environment(
        account=os.getenv('CDK_DEFAULT_ACCOUNT'),
        region=os.getenv('CDK_DEFAULT_REGION')
    )
)

app.synth()
