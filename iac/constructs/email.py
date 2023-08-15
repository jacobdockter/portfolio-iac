"""email.py
Email Construct Class
"""
from constructs import Construct

class Email(Construct):
    """
    Defines that resources that make up a Email forwarder
    """
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        project_name: str,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        print(f'Creating Email Forwarder for {project_name}')

        # TODO: Email Setup
        # TODO Lambda, Bucket, SES: 2 verified identities and a rule set, iam role + policy
