#!/usr/bin/env python3
import os

import aws_cdk as cdk

from iac.constants import CODESTAR_ARN, GITHUB_ACCOUNT, DOMAIN_ZONE_ID, BASE_DOMAIN
from iac.portfolio_stack import PortfolioStack

app = cdk.App()

PortfolioStack(
    app,
    "PortfolioStack",
    codestar_arn=CODESTAR_ARN,
    github_account=GITHUB_ACCOUNT,
    base_domain=BASE_DOMAIN,
    domain_zone_id=DOMAIN_ZONE_ID,
    env=cdk.Environment(
        account=os.getenv('CDK_DEFAULT_ACCOUNT'),
        region=os.getenv('CDK_DEFAULT_REGION')
    )
)

app.synth()
