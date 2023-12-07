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

        github_secret = Secret(
            self,
            "PortfolioGitHubInformationSecret",
            "GitHubInformation",
            body={
                "CODESTAR_ARN": SecretValue.unsafe_plain_text(""),
                "GITHUB_ACCOUNT": SecretValue.unsafe_plain_text("")
            }
        )

        domain_information_secret = Secret(
            self,
            "PortfolioDomainInformationSecret",
            "DomainInformation",
            body={
                "DOMAIN_NAME": SecretValue.unsafe_plain_text(""),
                "DOMAIN_ZONE_ID": SecretValue.unsafe_plain_text("")
            }
        )

        self.codestar_arn = github_secret.secret.secret_value_from_json('CODESTAR_ARN')
        self.github_account = github_secret.secret.secret_value_from_json('GITHUB_ACCOUNT')
        self.domain_name = domain_information_secret.secret.secret_value_from_json('DOMAIN_NAME')
        self.domain_zone_id = domain_information_secret.secret.secret_value_from_json('DOMAIN_ZONE_ID')
