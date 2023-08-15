from aws_cdk import (
    Stack,
)
from constructs import Construct
from iac.constructs.dns import DNS
from iac.constructs.cdn import CDN
from iac.constructs.client_pipeline import ClientPipeline

class PortfolioIacStack(Stack):
    """
    PortfolioIacStack
    Defines resources for the portfolio suite of applications
    """
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        codestar_arn,
        github_account,
        base_domain,
        domain_zone_id,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create dns construct
        dns = DNS(
            self,
            "DNS",
            "Portfolio",
            base_domain=base_domain,
            domain_zone_id=domain_zone_id
        )

        # create cdn bucket
        CDN(
            self,
            "CDN",
            "CDN",
            dns.zone,
            base_domain,
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
            base_domain,
            dns.certificate,
            "voice."
        )

        # create voice client pipeline
        ClientPipeline(
            self,
            "VoiceClientPipeline",
            "Voice",
            github_account,
            codestar_arn,
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
            base_domain,
            dns.certificate,
            "dev."
        )

        # create dev client pipeline
        ClientPipeline(
            self,
            "DevClientPipeline",
            "Dev",
            github_account,
            codestar_arn,
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
            base_domain,
            dns.certificate,
            ""
        )

        # create directory client pipeline
        ClientPipeline(
            self,
            "DirectoryClientPipeline",
            "Directory",
            github_account,
            codestar_arn,
            directory_client.client_bucket,
            directory_client.distribution,
            "directory-portfolio-client"
        )

        # TODO: Email Setup
        # TODO Lambda, Bucket, SES: 2 verified identities and a rule set, iam role + policy
