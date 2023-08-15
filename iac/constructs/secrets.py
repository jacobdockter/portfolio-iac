"""secrets.py
Secrets Construct Class
"""
from constructs import Construct

class Secrets(Construct):
    """
    Defines that resources that make up Secrets
    """
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        project_name: str,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        print(f'Creating Secrets for {project_name}')

        # TODO: secrets
