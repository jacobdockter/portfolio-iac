"""client_pipeline.py
Client Pipeline Construct Class
"""
from aws_cdk import (
    RemovalPolicy,
    aws_s3 as s3,
    aws_iam as iam,
    pipelines
)
from constructs import Construct

class IacPipeline(Construct):
    """
    Defines the resources that make up a iac pipeline
    """
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        resource_name: str,
        repository,
        github_account: str,
        codestar_arn: str,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        artifact_bucket = s3.Bucket(
            self,
            resource_name + 'ArtifactsBucket',
            bucket_name=f"{resource_name}-artifacts",
            removal_policy=RemovalPolicy.DESTROY,
            block_public_access = s3.BlockPublicAccess.BLOCK_ALL
        )

        codepipeline_role = iam.Role(
            self,
            f"{resource_name}CodePipelineRole",
            assumed_by=iam.ServicePrincipal("codepipeline.amazonaws.com"),
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess")
            ]
        )

        pipelines.CodePipeline(self, f"{resource_name}CdkPipeline",
            pipeline_name=f"{resource_name}CdkPipeline",
            artifact_bucket=artifact_bucket,
            role=codepipeline_role,
            synth=pipelines.ShellStep(
                "Synth",
                input=pipelines.CodePipelineSource.connection(
                    f"{github_account}/{repository}",
                    "main",
                    connection_arn=codestar_arn
                ),
                commands=[
                    "npm install -g aws-cdk",
                    "python -m pip install -r requirements.txt",
                    "cdk synth"
                ]
            )
        )
