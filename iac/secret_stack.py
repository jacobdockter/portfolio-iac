"""Secret_stack.py
Defines the SecretStack class
"""
from aws_cdk import (
    Stack,
)
from constructs import Construct
from iac.constructs.secret import Secret


class SecretStack(Stack):
    """
    SecretStack
    Defines resources for the applications Secrets
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        github_secret = Secret(
            self,
            "PortfolioCodeStarArnSecert",
            "CodeStarArn",
            body={"CODESTAR_ARN": "", "GITHUB_ACCOUNT": ""},
        )

        domain_information_secret = Secret(
            self,
            "PortfolioDomainInformationSecret",
            "DomainInformation",
            body={"DOMAIN_NAME": "", "DOMAIN_ZONE_ID": ""},
        )

        self.codestar_arn = github_secret.secret.secret_value_from_json("CODESTAR_ARN")
        self.github_account = github_secret.secret.secret_value_from_json(
            "GITHUB_ACCOUNT"
        )
        self.domain_name = domain_information_secret.secret.secret_value_from_json(
            "DOMAIN_NAME"
        )
        self.domain_zone_id = domain_information_secret.secret.secret_value_from_json(
            "DOMAIN_ZONE_ID"
        )
