import aws_cdk as cdk

from constructs_package.constants import AwsAccountId
from constructs_package.constants import AwsRegion
from constructs_package.constants import AwsStage
from infra.stack import SsoStack


app = cdk.App()

SsoStack(
    scope=app,
    id=f"Sso-{AwsStage.MANAGEMENT}",
    env=cdk.Environment(
        account=AwsAccountId.MANAGEMENT, region=AwsRegion.US_EAST_1
    ),
)

app.synth()
