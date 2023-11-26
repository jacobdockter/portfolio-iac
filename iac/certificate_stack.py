"""certificate_stack.py
Defines the CertificateStack class
"""
from aws_cdk import (
    Stack,
)
from constructs import Construct
from iac.constructs.certificate import Certificate

class CertificateStack(Stack):
    """
    CertificateStack
    Defines resources for the application certificate
    """
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # create certificate construct
        certificate = Certificate(
            self,
            "PortfolioCertificate",
            "Portfolio"
        )

        # output certificate and zone
        self.certificate = certificate.certificate
        self.zone = certificate.zone
