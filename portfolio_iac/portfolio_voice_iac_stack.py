from aws_cdk import (
    Stack,
    RemovalPolicy,
    Duration,
    aws_iam as iam,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_codebuild as codebuild,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_s3 as s3,
    aws_route53 as route53
)
from constructs import Construct

class PortfolioVoiceIacStack(Stack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        codestar_arn,
        github_account,
        base_domain,
        portfolio_zone,
        portfolio_certificate,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # client bucket to hold application
        client_bucket = s3.Bucket(
            self,
            'VoiceClientBucket',
            bucket_name=f"voice.{base_domain}",
            website_index_document='index.html',
            website_error_document='index.html',
            public_read_access=True,
            removal_policy=RemovalPolicy.DESTROY,
            cors=[
                s3.CorsRule(
                    allowed_origins=["*"],
                    allowed_methods=[s3.HttpMethods.GET]
                )
            ]
        )

        # create cloudfront distribution for delivery
        distribution = cloudfront.Distribution(
            self,
            'VoiceClientDistribution',
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(client_bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS
            ),
            domain_names=[f"voice.{base_domain}"],
            certificate=portfolio_certificate
        )

        # route cloudfront traffic to custom client domain
        route53.CnameRecord(
            self,
            'VoiceClientS3Domain',
            zone=portfolio_zone,
            record_name="voice",
            domain_name=distribution.distribution_domain_name
        )

        # source output/action for pipeline - pulls from github repo
        source_output = codepipeline.Artifact()
        source_action = codepipeline_actions.CodeStarConnectionsSourceAction(
            action_name="VoiceClientCodeStarSource",
            owner=github_account,
            repo="voice-portfolio-client",
            output=source_output,
            connection_arn=codestar_arn
        )

        # build output/action for pipeline - builds client
        build_output = codepipeline.Artifact()
        build_action = codepipeline_actions.CodeBuildAction(
            action_name="Build",
            project=codebuild.PipelineProject(
                self,
                "voice-client-codebuild-project",
                build_spec=codebuild.BuildSpec.from_source_filename(
                    filename='buildspec.yml'
                ),
                description='Pipeline for CodeBuild',
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
            "VoiceClientGitHubPipeline",
            pipeline_name="VoiceClientGitHubPipeline",
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
