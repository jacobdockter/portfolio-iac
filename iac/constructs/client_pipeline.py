"""client_pipeline.py
Client Pipeline Construct Class
"""
from aws_cdk import (
    Duration,
    aws_iam as iam,
    aws_codebuild as codebuild,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions
)
from iac.constants import GITHUB_ACCOUNT, CODESTAR_ARN
from constructs import Construct

class ClientPipeline(Construct):
    """
    Defines the resources that make up a client pipeline
    """
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        resource_name: str,
        client_bucket,
        distribution,
        repository,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # source output/action for pipeline - pulls from github repo
        source_output = codepipeline.Artifact()
        source_action = codepipeline_actions.CodeStarConnectionsSourceAction(
            action_name=f"{resource_name}CodeStarSource",
            owner=GITHUB_ACCOUNT,
            repo=repository,
            output=source_output,
            connection_arn=CODESTAR_ARN
        )

        # build output/action for pipeline - builds client
        build_output = codepipeline.Artifact()
        build_action = codepipeline_actions.CodeBuildAction(
            action_name="Build",
            project=codebuild.PipelineProject(
                self,
                f"{resource_name}ClientCodeBuildProject",
                build_spec=codebuild.BuildSpec.from_source_filename(
                    filename='buildspec.yml'
                ),
                description=f'Pipeline for {resource_name} Client CodeBuild',
                timeout=Duration.minutes(60),
                environment=codebuild.BuildEnvironment(
                    build_image=codebuild.LinuxBuildImage.STANDARD_6_0,
                    privileged=True
                ),
            ),
            input=source_output,
            outputs=[build_output],
            run_order=1
        )

        # deploy action for pipeline - deploys application to s3 bucket
        deploy_action = codepipeline_actions.S3DeployAction(
            action_name="Deploy",
            input=build_output,
            bucket=client_bucket
        )

        # Create the build project that will invalidate the cache
        invalidate_build_project = codebuild.PipelineProject(
            self,
            "InvalidateProject",
            build_spec=codebuild.BuildSpec.from_object({
                "version": "0.2",
                "phases": {
                    "build": {
                        "commands": [
                            'aws cloudfront create-invalidation --distribution-id ${CLOUDFRONT_ID} --paths "/*"'
                        ]
                    }
                }
            }),
            environment_variables={
                "CLOUDFRONT_ID": codebuild.BuildEnvironmentVariable(
                    value=distribution.distribution_id
                )
            }
        )

        # invalidate action for pipeline - invalidates cache on build to instantly reflect changes
        invalidate_action = codepipeline_actions.CodeBuildAction(
            action_name="InvalidateCache",
            project=invalidate_build_project,
            input=build_output,
            run_order=2
        )

        # add Cloudfront invalidation permissions to the project
        distribution_arn = f"arn:aws:cloudfront::{self.account}:distribution/{distribution.distribution_id}"
        invalidate_build_project.add_to_role_policy(iam.PolicyStatement(
            resources=[distribution_arn],
            actions=[
                "cloudfront:CreateInvalidation"
            ]
        ))

        # client pipeline
        codepipeline.Pipeline(
            self,
            f"{resource_name}ClientGitHubPipeline",
            pipeline_name=f"{resource_name}ClientGitHubPipeline",
            stages=[
                codepipeline.StageProps(
                    stage_name="Source",
                    actions=[
                        source_action
                    ]
                ),
                codepipeline.StageProps(
                    stage_name="Build",
                    actions=[
                        build_action
                    ],
                ),
                codepipeline.StageProps(
                    stage_name="Deploy",
                    actions=[
                        deploy_action,
                        invalidate_action
                    ]
                )
            ]
        )
