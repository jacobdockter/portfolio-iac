#!/usr/bin/env python3
import os

import aws_cdk as cdk

from portfolio_iac.constants import CODESTAR_ARN, GITHUB_ACCOUNT, DOMAIN_ZONE_ID, BASE_DOMAIN
from portfolio_iac.portfolio_directory_iac_stack import PortfolioDirectoryIacStack
from portfolio_iac.portfolio_voice_iac_stack import PortfolioVoiceIacStack
from portfolio_iac.portfolio_cdn_iac_stack import PortfolioCdnIacStack

app = cdk.App()

directory = PortfolioDirectoryIacStack(
    app,
    "PortfolioDirectoryIacStack",
    base_domain=BASE_DOMAIN,
    domain_zone_id=DOMAIN_ZONE_ID,
    env=cdk.Environment(
        account=os.getenv('CDK_DEFAULT_ACCOUNT'),
        region=os.getenv('CDK_DEFAULT_REGION')
    )
)

PortfolioCdnIacStack(
    app,
    "PortfolioCdnIacStack",
    base_domain=BASE_DOMAIN,
    portfolio_zone=directory.portfolio_zone,
    portfolio_certificate=directory.portfolio_certificate,
    env=cdk.Environment(
        account=os.getenv('CDK_DEFAULT_ACCOUNT'),
        region=os.getenv('CDK_DEFAULT_REGION')
    )
)

PortfolioVoiceIacStack(
    app,
    "PortfolioVoiceIacStack",
    codestar_arn=CODESTAR_ARN,
    github_account=GITHUB_ACCOUNT,
    base_domain=BASE_DOMAIN,
    portfolio_zone=directory.portfolio_zone,
    portfolio_certificate=directory.portfolio_certificate,
    env=cdk.Environment(
        account=os.getenv('CDK_DEFAULT_ACCOUNT'),
        region=os.getenv('CDK_DEFAULT_REGION')
    )
)


app.synth()
