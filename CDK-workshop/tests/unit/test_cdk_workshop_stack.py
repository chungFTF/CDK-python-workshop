import aws_cdk as core
import aws_cdk.assertions as assertions

from cdk_workshop.cdk_workshop_stack import CdkWorkshopStack

# example tests. To run these tests, uncomment this file along with the example
# resource in cdk_workshop/cdk_workshop_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = CdkWorkshopStack(app, "cdk-workshop")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
