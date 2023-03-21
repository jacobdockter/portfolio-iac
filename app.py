#!/usr/bin/env python3
import os

import aws_cdk as cdk

from voice_portfolio_iac.voice_portfolio_iac_stack import VoicePortfolioIacStack


app = cdk.App()
VoicePortfolioIacStack(
    app,
    "VoicePortfolioIacStack",
    env=cdk.Environment(
        account=os.getenv('CDK_DEFAULT_ACCOUNT'),
        region=os.getenv('CDK_DEFAULT_REGION')
    ),
)

app.synth()
