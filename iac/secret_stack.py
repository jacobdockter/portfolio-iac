"""Secret_stack.py
Defines the SecretStack class
"""
from aws_cdk import (
    Stack,
    SecretValue
)
from constructs import Construct
from iac.constructs.secret import Secret

class SecretStack(Stack):
    """
    SecretStack
    Defines resources for the applications Secrets
    """
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        domain_information_secret = Secret(
            self,
            "PortfolioDomainZoneSecret",
            "DomainZoneID",
            body=""
        )

        self.domain_zone_id = domain_information_secret.secret.secret_value.to_string()
