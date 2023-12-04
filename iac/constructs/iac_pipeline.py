"""client_pipeline.py
Client Pipeline Construct Class
"""
from aws_cdk import RemovalPolicy, aws_s3 as s3, pipelines
from constructs import Construct
from iac.constants import GITHUB_ACCOUNT, CODESTAR_ARN


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
        **kwargs,
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        artifact_bucket = s3.Bucket(
            self,
            resource_name + "ArtifactsBucket",
            bucket_name=f"{resource_name}-artifacts",
            removal_policy=RemovalPolicy.DESTROY,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL,
        )

        pipelines.CodePipeline(
            self,
            f"{resource_name}CdkPipeline",
            pipeline_name=f"{resource_name}CdkPipeline",
            artifact_bucket=artifact_bucket,
            synth=pipelines.ShellStep(
                "Synth",
                input=pipelines.CodePipelineSource.connection(
                    f"{GITHUB_ACCOUNT}/{repository}",
                    "main",
                    connection_arn=CODESTAR_ARN,
                ),
                commands=[
                    "npm install -g aws-cdk",
                    "python -m pip install -r requirements.txt",
                    "cdk synth",
                ],
            ),
        )
