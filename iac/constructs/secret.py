"""secret.py
Secret Construct Class
"""
from constructs import Construct


class Secret(Construct):
    """
    Defines that resources that make up a Secret
    """

    def __init__(
        self, scope: Construct, construct_id: str, project_name: str, **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        print(f"Creating Secret for {project_name}")

        # TODO: secrets
