from aws_cdk import (
    Stack,
    aws_certificatemanager as acm,
    aws_route53 as route53
)
from constructs import Construct

class PortfolioDirectoryIacStack(Stack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        domain_zone_id,
        base_domain,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # retrieve domain zonr from route53
        self.portfolio_zone = route53.HostedZone.from_hosted_zone_attributes(
            self,
            "PortfolioDomainZone",
            hosted_zone_id=domain_zone_id,
            zone_name=base_domain
        )

        # create certificate validated by zone
        self.portfolio_certificate = acm.Certificate(
            self,
            'PortfolioCertificate',
            certificate_name=f"{base_domain}",
            domain_name=f"*.{base_domain}",
            validation=acm.CertificateValidation.from_dns(self.portfolio_zone)
        )
