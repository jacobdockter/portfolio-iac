"""certificate.py
Certificate Construct Class
"""
from aws_cdk import (
    aws_certificatemanager as acm,
    aws_route53 as route53
)
from constructs import Construct

class Certificate(Construct):
    """
    Defines that resources that make up a Certificate
    """
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        project_name: str,
        base_domain: str,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # retrieve domain zone from route53
        self.zone = route53.HostedZone.from_lookup(
            self,
            project_name + "DomainZone",
            domain_name=base_domain
        )

        # create certificate validated by zone
        self.certificate = acm.Certificate(
            self,
            project_name + "Certificate",
            certificate_name=base_domain,
            domain_name=base_domain,
            subject_alternative_names=[f"*.{base_domain}"],
            validation=acm.CertificateValidation.from_dns(self.zone),
        )
