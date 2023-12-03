"""api_pipeline.py
Api Pipeline Construct Class
"""
import os
from aws_cdk import (
    RemovalPolicy,
    Duration,
    aws_iam as iam,
    aws_codebuild as codebuild,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions
)
from constructs import Construct
from iac.constants import GITHUB_ACCOUNT, CODESTAR_ARN

class ApiPipeline(Construct):
    """
    Defines the resources that make up a api pipeline
    """
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        resource_name: str,
        repository,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        pass
