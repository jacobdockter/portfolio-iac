"""client_pipeline.py
Client Pipeline Construct Class
"""
import os
from aws_cdk import (
    RemovalPolicy,
    Duration,
    aws_iam as iam,
    aws_s3 as s3,
    aws_codebuild as codebuild,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions
)
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
        github_account: str,
        codestar_arn: str,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # source output/action for pipeline - pulls from github repo
        source_output = codepipeline.Artifact()
        source_action = codepipeline_actions.CodeStarConnectionsSourceAction(
            action_name=f"{resource_name}CodeStarSource",
            owner=github_account,
            repo=repository,
            output=source_output,
            connection_arn=codestar_arn
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
        distribution_arn = f"arn:aws:cloudfront::{os.getenv('CDK_DEFAULT_ACCOUNT')}:distribution/{distribution.distribution_id}"
        invalidate_build_project.add_to_role_policy(iam.PolicyStatement(
            resources=[distribution_arn],
            actions=[
                "cloudfront:CreateInvalidation"
            ]
        ))

        # TODO: use lambda to invalidate cache instead of codebuild
        # invalidate action for pipeline - invalidates cloudfront cache
        # invalidate_action = codepipeline_actions.LambdaInvokeAction(
        #     action_name="InvalidateCache",
        #     lambda_=invalidation_lambda,
        #     user_parameters=distribution.distribution_id,
        #     run_order=2
        # )

        # # add Lambda invoke permissions to invalidate action
        # invalidate_action.action_properties.role.add_to_policy(
        #     iam.PolicyStatement(
        #         actions=["lambda:InvokeFunction", "lambda:ListFunctions"],
        #         resources=[invalidation_lambda.function_arn]
        #     )
        # )

        artifact_bucket = s3.Bucket(
            self,
            resource_name + 'ArtifactsBucket',
            bucket_name=f"{resource_name}-artifacts",
            removal_policy=RemovalPolicy.DESTROY,
            block_public_access = s3.BlockPublicAccess.BLOCK_ALL
        )

        # client pipeline
        codepipeline.Pipeline(
            self,
            f"{resource_name}ClientGitHubPipeline",
            pipeline_name=f"{resource_name}ClientGitHubPipeline",
            artifact_bucket=artifact_bucket,
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
