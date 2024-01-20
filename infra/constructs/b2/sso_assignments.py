from aws_cdk import aws_iam as iam
from constructs import Construct
from constructs_package.constants import AwsAccountId
from infra.constructs.b1.sso import B1AdministratorAccess
from infra.constructs.b1.sso import B1BillingAccess
from infra.constructs.b1.sso import B1PowerUserAccess
from infra.constructs.b1.sso import B1ReadOnlyAccess
from infra.constructs.l2.sso import AccountTarget
from infra.constructs.l2.sso import GroupPrincipal
from infra.constructs.l2.sso import SsoInstance


# Hardcoding the SSO instance ARN here copied from the AWS console
sso_instance = SsoInstance(
    "arn:aws:sso:::instance/ssoins-7223396617db918e",
)

production = AccountTarget(AwsAccountId.PRODUCTION)
staging = AccountTarget(AwsAccountId.STAGING)
sandbox = AccountTarget(AwsAccountId.SANDBOX)
management = AccountTarget(AwsAccountId.MANAGEMENT)

# We have to create groups in the console and paste the group IDs here
# It's not possible to create groups with CDK or Cloudformation
engineers_group = GroupPrincipal(
    "94884448-b0d1-709b-f585-5ebc6418605b",
)
administrators_group = GroupPrincipal(
    "84186448-30f1-704e-3f55-0250723c3f3d",
)
finance_group = GroupPrincipal(
    "d4789478-4051-70c2-45b3-eeda94485995",
)


class B2SsoAssignments(Construct):
    """Cloudfront Firewall"""

    def __init__(self, scope: Construct, id: str) -> None:
        super().__init__(scope, id)

        # Read Only Permissions
        read_only = B1ReadOnlyAccess(
            scope=self,
            id="ReadOnly",
            sso_instance=sso_instance,
            inline_policy=iam.PolicyDocument(
                statements=[
                    iam.PolicyStatement(
                        effect=iam.Effect.ALLOW,
                        actions=["lambda:InvokeFunction"],
                        resources=["*"],
                    )
                ]
            ),
        )
        read_only.create_assignment(
            principal=engineers_group,
            targets=[production, staging, sandbox],
        )

        # Power User Permissions
        power_user = B1PowerUserAccess(
            scope=self,
            id="PowerUser",
            sso_instance=sso_instance,
        )
        power_user.create_assignment(
            principal=engineers_group,
            targets=[sandbox],
        )

        # Administrator Permissions
        administrator = B1AdministratorAccess(
            scope=self,
            id="Administrator",
            sso_instance=sso_instance,
        )
        administrator.create_assignment(
            principal=administrators_group,
            targets=[
                production,
                staging,
                sandbox,
                management,
            ],
        )

        # Billing Permissions
        billing = B1BillingAccess(
            scope=self,
            id="Billing",
            sso_instance=sso_instance,
        )
        billing.create_assignment(
            principal=finance_group,
            targets=[management],
        )
