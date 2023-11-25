"""cdn.py
CDN Construct Class
"""
from aws_cdk import (
    RemovalPolicy,
    aws_route53 as route53,
    aws_route53_targets as route53_targets,
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins
)
from constructs import Construct
from iac.constants import BASE_DOMAIN

class CDN(Construct):
    """
    Defines resources that make up a CDN.
    """
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        resource_name: str,
        zone,
        certificate,
        sub_domain: str,
        storage: bool = False,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        prefix = '' if sub_domain == '' else sub_domain + '.'
        alias_record_name = BASE_DOMAIN if sub_domain == '' else sub_domain

        # client bucket to hold application
        if storage:
            self.client_bucket = s3.Bucket(
                self,
                resource_name + 'Bucket',
                bucket_name=resource_name,
                removal_policy=RemovalPolicy.DESTROY,
                block_public_access = s3.BlockPublicAccess.BLOCK_ALL
            )
        else:
            self.client_bucket = s3.Bucket(
                self,
                resource_name + 'Bucket',
                bucket_name=f"{prefix}{BASE_DOMAIN}",
                website_index_document='index.html',
                website_error_document='index.html',
                public_read_access=True,
                block_public_access=s3.BlockPublicAccess(
                    block_public_acls=False,
                    block_public_policy=False,
                    ignore_public_acls=False,
                    restrict_public_buckets=False
                ),
                removal_policy=RemovalPolicy.DESTROY,
                cors=[
                    s3.CorsRule(
                        allowed_origins=["*"],
                        allowed_methods=[s3.HttpMethods.GET]
                    )
                ]
            )

        # create cloudfront distribution for delivery

        self.distribution = cloudfront.Distribution(
            self,
            resource_name + 'Distribution',
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(self.client_bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS
            ),
            domain_names=[f"{prefix}{BASE_DOMAIN}"],
            certificate=certificate,
        )

        # route cloudfront traffic to custom client domain
        route53.ARecord(
            self,
            resource_name + 'Domain',
            zone=zone,
            record_name=alias_record_name,
            target=route53.RecordTarget.from_alias(
                route53_targets.CloudFrontTarget(self.distribution)
            )
        )
