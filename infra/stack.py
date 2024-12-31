import aws_cdk as cdk

from constructs import Construct
from infra.constructs.b2.organization import B2Organization
from infra.constructs.b2.sso_assignments import B2SsoAssignments


class OrgsSsoStack(cdk.Stack):
    """Create the AWS Organizations and SSO resources"""

    def __init__(
        self,
        scope: Construct,
        id: str,
        **kwargs,
    ) -> None:
        super().__init__(scope, id, **kwargs)

        organization = B2Organization(
            scope=self,
            id="Organization",
        )

        B2SsoAssignments(
            scope=self,
            id="SsoAssignments",
            organization=organization,
        )

        # Add tags to everything in this stack
        cdk.Tags.of(self).add(key="owner", value="Platform")
        cdk.Tags.of(self).add(key="repo", value="ch-orgs-sso")
        cdk.Tags.of(self).add(key="stack", value=self.stack_name)
