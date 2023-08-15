"""dns.py
DNS Construct Class
"""
from aws_cdk import (
    aws_certificatemanager as acm,
    aws_route53 as route53
)
from constructs import Construct
from iac.constants import DOMAIN_ZONE_ID, BASE_DOMAIN

class DNS(Construct):
    """
    Defines that resources that make up a DNS
    """
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        project_name: str,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # retrieve domain zone from route53
        self.zone = route53.HostedZone.from_hosted_zone_attributes(
            self,
            project_name + "DomainZone",
            hosted_zone_id=DOMAIN_ZONE_ID,
            zone_name=BASE_DOMAIN
        )

        # create certificate validated by zone
        self.certificate = acm.Certificate(
            self,
            project_name + "Certificate",
            certificate_name=f"{BASE_DOMAIN}",
            domain_name=f"*.{BASE_DOMAIN}",
            validation=acm.CertificateValidation.from_dns(self.zone)
        )
