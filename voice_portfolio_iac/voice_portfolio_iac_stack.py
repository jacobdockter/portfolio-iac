from aws_cdk import (
    Stack,
    RemovalPolicy,
    Duration,
    CfnOutput,
    aws_iam as iam,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_codebuild as codebuild,
    aws_codepipeline as codepipeline,
    aws_codepipeline_actions as codepipeline_actions,
    aws_s3 as s3,
    aws_certificatemanager as acm,
    aws_route53 as route53
)
from constructs import Construct

class VoicePortfolioIacStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        codestar_arn = "arn:aws:codestar-connections:us-east-1:519292530037:connection/5b4f0d41-8af8-49b2-918b-8955b97aee9d"
        github_account = "jacobdockter"
        domain_zone_id = "Z04599073ANR3P6TNUUQD"
        base_domain = "jacobdockter.com"

        # retrieve domain zonr from route53
        zone = route53.HostedZone.from_hosted_zone_attributes(
            self,
            "VoiceDomainZone",
            hosted_zone_id=domain_zone_id,
            zone_name=base_domain
        )

        # create certificate validated by zone
        portfolio_certificate = acm.Certificate(
            self,
            'VoiceClientCertificate',
            certificate_name=f"voice.{base_domain}",
            domain_name=f"voice.{base_domain}",
            validation=acm.CertificateValidation.from_dns(zone)
        )

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
            zone=zone,
            record_name="app",
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
        pipeline = codepipeline.Pipeline(
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

        # Outputs
        CfnOutput(
            self,
            'VoiceCertificate',
            value=portfolio_certificate.certificate_arn,
            description="Voice Certificate"
        )

        CfnOutput(
            self,
            'VoiceClientURL',
            value=client_bucket.bucket_website_url,
            description="Client S3 Bucket URL"
        )

        CfnOutput(
            self,
            'VoiceClientDist',
            value=distribution.distribution_domain_name,
            description="Client CloudFront Distribution"
        )

        CfnOutput(
            self,
            "VoicePipelineOut",
            description="Code Pipeline",
            value=pipeline.pipeline_name
        )
