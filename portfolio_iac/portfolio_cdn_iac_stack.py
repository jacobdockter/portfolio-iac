from aws_cdk import (
    Stack,
    RemovalPolicy,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_s3 as s3,
    aws_route53 as route53
)
from constructs import Construct

class PortfolioCdnIacStack(Stack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        base_domain,
        portfolio_zone,
        portfolio_certificate,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # client bucket to hold application
        client_bucket = s3.Bucket(
            self,
            'PortfolioCdnBucket',
            bucket_name=f"cdn.{base_domain}",
            removal_policy=RemovalPolicy.DESTROY,
            block_public_access = s3.BlockPublicAccess.BLOCK_ALL
        )

        # create cloudfront distribution for delivery
        distribution = cloudfront.Distribution(
            self,
            'PortfolioCdnDistribution',
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(client_bucket),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS
            ),
            domain_names=[f"cdn.{base_domain}"],
            certificate=portfolio_certificate
        )

        # route cloudfront traffic to custom client domain
        route53.CnameRecord(
            self,
            'PortfolioCdnS3Domain',
            zone=portfolio_zone,
            record_name="cdn",
            domain_name=distribution.distribution_domain_name
        )
