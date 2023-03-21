import aws_cdk as core
import aws_cdk.assertions as assertions

from voice_portfolio_iac.voice_portfolio_iac_stack import VoicePortfolioIacStack

# example tests. To run these tests, uncomment this file along with the example
# resource in portfolio_iac/portfolio_iac_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = VoicePortfolioIacStack(app, "voice-portfolio-iac")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
