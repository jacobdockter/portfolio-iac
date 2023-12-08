"""Secret_stack.py
Defines the SecretStack class
"""
from aws_cdk import Stack, SecretValue
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
            self, "PortfolioCodestarArnSecret", "CodestarArn", body=""
        )

        domain_information_secret = Secret(
            self,
            "PortfolioDomainInformationSecret",
            "DomainInformation",
            body={
                "DOMAIN_NAME": SecretValue.unsafe_plain_text(""),
                "DOMAIN_ZONE_ID": SecretValue.unsafe_plain_text(""),
            },
        )

        self.codestar_arn = github_secret.secret.secret_value.to_string()
        self.domain_name = domain_information_secret.secret.secret_value_from_json(
            "DOMAIN_NAME"
        ).to_string()
        self.domain_zone_id = domain_information_secret.secret.secret_value_from_json(
            "DOMAIN_ZONE_ID"
        ).to_string()
