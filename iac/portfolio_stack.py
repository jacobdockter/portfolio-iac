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
    GITHUB_ACCOUNT,
    RESOURCE_NAME
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
        certificate_stack,
        secret_stack,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create iac pipeline
        IacPipeline(
            self,
            "PortfolioIacPipeline",
            "portfolio-iac-pipeline",
            "portfolio-iac",
            GITHUB_ACCOUNT,
            secret_stack.codestar_arn
        )

        # create cdn bucket
        CDN(
            self,
            "PortfolioCDN",
            f"{RESOURCE_NAME}-portfolio-cdn",
            certificate_stack.zone,
            certificate_stack.certificate,
            "cdn",
            secret_stack.base_domain,
            True
        )

        # create voice client bucket
        voice_client = CDN(
            self,
            "VoiceClient",
            f"{RESOURCE_NAME}-voice-client",
            certificate_stack.zone,
            certificate_stack.certificate,
            "voice",
            secret_stack.base_domain,
            False
        )

        # create voice client pipeline
        ClientPipeline(
            self,
            "VoiceClientPipeline",
            f"{RESOURCE_NAME}-voice-client-pipeline",
            voice_client.client_bucket,
            voice_client.distribution,
            VOICE_CLIENT_REPOSITORY,
            GITHUB_ACCOUNT,
            secret_stack.codestar_arn
        )


        # create dev client bucket
        dev_client = CDN(
            self,
            "DevClient",
            f"{RESOURCE_NAME}-dev-client",
            certificate_stack.zone,
            certificate_stack.certificate,
            "dev",
            secret_stack.base_domain,
            False
        )

        # create dev client pipeline
        ClientPipeline(
            self,
            "DevClientPipeline",
            f"{RESOURCE_NAME}-dev-client-pipeline",
            dev_client.client_bucket,
            dev_client.distribution,
            DEV_CLIENT_REPOSITORY,
            GITHUB_ACCOUNT,
            secret_stack.codestar_arn
        )

        # create directory client bucket
        directory_client = CDN(
            self,
            "DirectoryClient",
            f"{RESOURCE_NAME}-directory-client",
            certificate_stack.zone,
            certificate_stack.certificate,
            "",
            secret_stack.base_domain,
            False
        )

        # create directory client pipeline
        ClientPipeline(
            self,
            "DirectoryClientPipeline",
            f"{RESOURCE_NAME}-directory-client-pipeline",
            directory_client.client_bucket,
            directory_client.distribution,
            DIRECTORY_CLIENT_REPOSITORY,
            GITHUB_ACCOUNT,
            secret_stack.codestar_arn
        )
