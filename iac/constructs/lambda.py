"""lambda.py
Client Pipeline Construct Class
"""
from os import path
from aws_cdk import (
    Duration,
    RemovalPolicy,
    aws_lambda as _lambda,
    aws_logs as logs,
    aws_iam as iam,
)
from constructs import Construct

__dirname = path.dirname(__file__)


class Lambda(Construct):
    """
    Defines the resources that make up a lambda
    """
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        resource_name: str,
        description: str,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # c# lambda function
        self.lambda_function = _lambda.Function(
            self,
            f"{resource_name}LambdaFunction",
            runtime=_lambda.Runtime.DOTNET_CORE_3_1,
            code=_lambda.Code.from_asset(path.join(__dirname, "templates/lambda.zip")),
            handler='lambda::lambda.Function::FunctionHandlerAsync',
            timeout=Duration.seconds(30),
            memory_size=256,
            description=f'{description}. Managed by CDK.',
            function_name=f'{resource_name}LambdaFunction'
        )

        # cloudwatch log group
        self.log_group = logs.LogGroup(
            self,
            f"{resource_name}LogGroup",
            log_group_name=f"/aws/lambda/{resource_name}LambdaFunction",
            removal_policy=RemovalPolicy.DESTROY
        )

        # lambda iam role
        self.iam_role = iam.Role(
            self,
            f"{resource_name}LambdaRole",
            assumed_by=iam.ServicePrincipal('lambda.amazonaws.com'),
            description=f'{description} lambda role. Managed by CDK.',
            role_name=f'{resource_name}LambdaRole'
        )

        # lambda iam policy
        self.iam_policy = iam.Policy(
            self,
            f"{resource_name}LambdaPolicy",
            statements=[
                iam.PolicyStatement(
                    actions=[
                        'logs:CreateLogGroup',
                        'logs:CreateLogStream',
                        'logs:PutLogEvents',
                    ],
                    resources=[
                        self.log_group.log_group_arn,
                        f'{self.log_group.log_group_arn}:*'
                    ]
                )
            ],
            roles=[self.iam_role]
        )
