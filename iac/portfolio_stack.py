"""portfolio_stack.py
Defines the PortfolioIacStack class
"""
from aws_cdk import (
    Stack,
)
from constructs import Construct
from iac.constructs.cdn import CDN
from iac.constructs.client_pipeline import ClientPipeline
from iac.constructs.iac_pipeline import IacPipeline
from iac.constants import (
    DEV_CLIENT_REPOSITORY,
    DIRECTORY_CLIENT_REPOSITORY,
    VOICE_CLIENT_REPOSITORY,
    IAC_REPOSITORY,
    GITHUB_ACCOUNT,
    CODESTAR_ARN,
    BASE_DOMAIN_NAME
)

class PortfolioIacStack(Stack):
    """
    PortfolioIacStack
    Defines resources for the portfolio suite of applications
    """
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        resource_name: str,
        certificate_stack,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create iac pipeline
        IacPipeline(
            self,
            "PortfolioIacPipeline",
            "portfolio-iac-pipeline",
            IAC_REPOSITORY,
            GITHUB_ACCOUNT,
            CODESTAR_ARN
        )

        # create cdn bucket
        CDN(
            self,
            "PortfolioCDN",
            f"{resource_name}-portfolio-cdn",
            certificate_stack.zone,
            certificate_stack.certificate,
            "cdn",
            BASE_DOMAIN_NAME,
            True
        )

        # create voice client bucket
        voice_client = CDN(
            self,
            "VoiceClient",
            f"{resource_name}-voice-client",
            certificate_stack.zone,
            certificate_stack.certificate,
            "voice",
            BASE_DOMAIN_NAME,
            False
        )

        # create voice client pipeline
        ClientPipeline(
            self,
            "VoiceClientPipeline",
            f"{resource_name}-voice-client-pipeline",
            voice_client.client_bucket,
            voice_client.distribution,
            VOICE_CLIENT_REPOSITORY,
            GITHUB_ACCOUNT,
            CODESTAR_ARN
        )


        # create dev client bucket
        dev_client = CDN(
            self,
            "DevClient",
            f"{resource_name}-dev-client",
            certificate_stack.zone,
            certificate_stack.certificate,
            "dev",
            BASE_DOMAIN_NAME,
            False
        )

        # create dev client pipeline
        ClientPipeline(
            self,
            "DevClientPipeline",
            f"{resource_name}-dev-client-pipeline",
            dev_client.client_bucket,
            dev_client.distribution,
            DEV_CLIENT_REPOSITORY,
            GITHUB_ACCOUNT,
            CODESTAR_ARN
        )

        # create directory client bucket
        directory_client = CDN(
            self,
            "DirectoryClient",
            f"{resource_name}-directory-client",
            certificate_stack.zone,
            certificate_stack.certificate,
            "",
            BASE_DOMAIN_NAME,
            False
        )

        # create directory client pipeline
        ClientPipeline(
            self,
            "DirectoryClientPipeline",
            f"{resource_name}-directory-client-pipeline",
            directory_client.client_bucket,
            directory_client.distribution,
            DIRECTORY_CLIENT_REPOSITORY,
            GITHUB_ACCOUNT,
            CODESTAR_ARN
        )
