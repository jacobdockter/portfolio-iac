"""portfolio_stack.py
Defines the PortfolioIacStack class
"""
from aws_cdk import (
    Stack,
)
from constructs import Construct
from iac.constructs.dns import DNS
from iac.constructs.cdn import CDN
from iac.constructs.client_pipeline import ClientPipeline
from iac.constructs.iac_pipeline import IacPipeline

class PortfolioIacStack(Stack):
    """
    PortfolioIacStack
    Defines resources for the portfolio suite of applications
    """
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create iac pipeline
        IacPipeline(
            self,
            "IacPipeline",
            "Portfolio",
            "portfolio-iac"
        )

        # create dns construct
        dns = DNS(
            self,
            "DNS",
            "Portfolio"
        )

        # create cdn bucket
        CDN(
            self,
            "CDN",
            "CDN",
            dns.zone,
            dns.certificate,
            "cdn.",
            True
        )

        # create voice client bucket
        voice_client = CDN(
            self,
            "VoiceClient",
            "VoiceClient",
            dns.zone,
            dns.certificate,
            "voice.",
            False
        )

        # create voice client pipeline
        ClientPipeline(
            self,
            "VoiceClientPipeline",
            "Voice",
            voice_client.client_bucket,
            voice_client.distribution,
            "voice-portfolio-client"
        )


        # create dev client bucket
        dev_client = CDN(
            self,
            "DevClient",
            "DevClient",
            dns.zone,
            dns.certificate,
            "dev.",
            False
        )

        # create dev client pipeline
        ClientPipeline(
            self,
            "DevClientPipeline",
            "Dev",
            dev_client.client_bucket,
            dev_client.distribution,
            "dev-portfolio-client"
        )

        # create directory client bucket
        directory_client = CDN(
            self,
            "DirectoryClient",
            "DirectoryClient",
            dns.zone,
            dns.certificate,
            "",
            False
        )

        # create directory client pipeline
        ClientPipeline(
            self,
            "DirectoryClientPipeline",
            "Directory",
            directory_client.client_bucket,
            directory_client.distribution,
            "directory-portfolio-client"
        )
