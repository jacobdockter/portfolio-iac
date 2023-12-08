"""secret.py
Secret Construct Class
"""
from constructs import Construct
from aws_cdk import RemovalPolicy, aws_secretsmanager as secretsmanager


class Secret(Construct):
    """
    Defines that resources that make up a Secret
    """

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        resource_name: str,
        body: dict = None,
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        if body is None:
            self.secret = secretsmanager.Secret(
                self,
                f"{resource_name}Secret",
                secret_name=f"{resource_name}Secret",
                description=f"{resource_name} Secret. Managed by CDK.",
                removal_policy=RemovalPolicy.DESTROY,
            )
        else:
            self.secret = secretsmanager.Secret(
                self,
                f"{resource_name}Secret",
                secret_name=f"{resource_name}Secret",
                description=f"{resource_name} Secret. Managed by CDK.",
                secret_object_value=body,
                removal_policy=RemovalPolicy.DESTROY,
            )
