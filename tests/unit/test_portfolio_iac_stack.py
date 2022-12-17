import aws_cdk as core
import aws_cdk.assertions as assertions

from portfolio_iac.portfolio_iac_stack import PortfolioIacStack

# example tests. To run these tests, uncomment this file along with the example
# resource in portfolio_iac/portfolio_iac_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = PortfolioIacStack(app, "portfolio-iac")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
