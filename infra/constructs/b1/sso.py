from typing import Optional

from aws_cdk import aws_iam as iam
from constructs import Construct
from infra.constructs.l2.sso import PermissionSet
from infra.constructs.l2.sso import SessionDuration
from infra.constructs.l2.sso import SsoInstance


class B1AdministratorAccess(PermissionSet):
    """Administrator Permission Set"""

    def __init__(
        self,
        scope: Construct,
        id: str,
        sso_instance: SsoInstance,
    ) -> None:
        super().__init__(
            scope=scope,
            id=id,
            sso_instance=sso_instance,
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AdministratorAccess"
                ),
            ],
            session_duration=SessionDuration.ONE_HOUR,
        )


class B1ReadOnlyAccess(PermissionSet):
    """Read Only Access Permission Set"""

    def __init__(
        self,
        scope: Construct,
        id: str,
        sso_instance: SsoInstance,
        inline_policy: Optional[iam.PolicyDocument] = None,
    ) -> None:
        super().__init__(
            scope=scope,
            id=id,
            sso_instance=sso_instance,
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "ReadOnlyAccess"
                ),
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "AWSBillingReadOnlyAccess"
                ),
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "CloudWatchLogsReadOnlyAccess"
                ),
            ],
            inline_policy=inline_policy,
            session_duration=SessionDuration.EIGHT_HOURS,
        )


class B1PowerUserAccess(PermissionSet):
    """Power User Access Permission Set"""

    def __init__(
        self,
        scope: Construct,
        id: str,
        sso_instance: SsoInstance,
    ) -> None:
        super().__init__(
            scope=scope,
            id=id,
            sso_instance=sso_instance,
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "PowerUserAccess"
                ),
            ],
            session_duration=SessionDuration.TWO_HOURS,
        )


class B1BillingAccess(PermissionSet):
    """Billing Access Permission Set"""

    def __init__(
        self,
        scope: Construct,
        id: str,
        sso_instance: SsoInstance,
    ) -> None:
        super().__init__(
            scope=scope,
            id=id,
            sso_instance=sso_instance,
            managed_policies=[
                iam.ManagedPolicy.from_aws_managed_policy_name(
                    "job-function/Billing"
                ),
            ],
            session_duration=SessionDuration.ONE_HOUR,
        )
