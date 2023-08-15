"""cdn.py
CDN Construct Class
"""
from aws_cdk import (
    RemovalPolicy,
    aws_certificatemanager as acm,
    aws_route53 as route53,
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

        # client bucket to hold application
        if storage:
            client_bucket = s3.Bucket(
                self,
                resource_name + 'Bucket',
                bucket_name=f"{sub_domain}{BASE_DOMAIN}",
                removal_policy=RemovalPolicy.DESTROY,
                block_public_access = s3.BlockPublicAccess.BLOCK_ALL
            )
        else:
            client_bucket = s3.Bucket(
                self,
                resource_name + 'Bucket',
                bucket_name=f"{sub_domain}{BASE_DOMAIN}",
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
            resource_name + 'Distribution',
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(client_bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS
            ),
            domain_names=[f"{sub_domain}{BASE_DOMAIN}"],
            certificate=certificate
        )

        # route cloudfront traffic to custom client domain
        route53.CnameRecord(
            self,
            resource_name + 'S3Domain',
            zone=zone,
            record_name=sub_domain,
            domain_name=distribution.distribution_domain_name
        )
