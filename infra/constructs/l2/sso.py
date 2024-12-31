from enum import StrEnum
from typing import Optional

import aws_cdk.aws_sso as sso

from aws_cdk import aws_iam as iam
from constructs import Construct


class SessionDuration(StrEnum):
    """Session duration for SSO"""

    ONE_HOUR = "PT1H"
    TWO_HOURS = "PT2H"
    FOUR_HOURS = "PT4H"
    EIGHT_HOURS = "PT8H"
    SIXTEEN_HOURS = "PT16H"
    TWENTY_FOUR_HOURS = "PT24H"


class PrincipalType(StrEnum):
    """Principal type for SSO"""

    USER = "USER"
    GROUP = "GROUP"


class TargetType(StrEnum):
    """Target type for SSO"""

    AWS_ACCOUNT = "AWS_ACCOUNT"


class Principal:
    """SSO Principal"""

    def __init__(self, principal_type: PrincipalType, principal_id: str) -> None:
        self.principal_type = principal_type
        self.principal_id = principal_id


class UserPrincipal(Principal):
    """SSO User Principal"""

    def __init__(self, user_id: str) -> None:
        super().__init__(
            principal_type=PrincipalType.USER,
            principal_id=user_id,
        )


class GroupPrincipal(Principal):
    """SSO Group Principal"""

    def __init__(self, group_id: str) -> None:
        super().__init__(
            principal_type=PrincipalType.GROUP,
            principal_id=group_id,
        )


class Target:
    """SSO Target"""

    def __init__(self, target_type: TargetType, target_id: str) -> None:
        self.target_type = target_type
        self.target_id = target_id


class AccountTarget(Target):
    """SSO Account Target"""

    def __init__(self, account_id: str) -> None:
        super().__init__(
            target_type=TargetType.AWS_ACCOUNT,
            target_id=account_id,
        )


class SsoInstance:
    """SSO Instance"""

    def __init__(self, instance_arn: str) -> None:
        self.sso_instance_arn = instance_arn


class PermissionSet(sso.CfnPermissionSet):
    """L2 construct for SSO Permission Set"""

    def __init__(
        self,
        scope: Construct,
        id: str,
        sso_instance: SsoInstance,
        managed_policies: list[iam.IManagedPolicy],
        inline_policy: Optional[iam.PolicyDocument] = None,
        session_duration: SessionDuration = SessionDuration.EIGHT_HOURS,
    ) -> None:
        self.sso_instance = sso_instance

        super().__init__(
            scope=scope,
            id=id,
            name=id,
            instance_arn=self.sso_instance.sso_instance_arn,
            managed_policies=[policy.managed_policy_arn for policy in managed_policies],
            inline_policy=inline_policy,
            session_duration=session_duration,
        )

    @property
    def permission_set_arn(self) -> str:
        """Return the permission set ARN"""
        return self.attr_permission_set_arn

    def create_assignment(
        self,
        principal: Principal,
        targets: list[Target],
    ) -> None:
        """Create assignments for the permission set"""

        for idx, target in enumerate(targets):
            Assignment(
                scope=self,
                id=f"Target{idx}",
                sso_instance=self.sso_instance,
                permission_set=self,
                principal=principal,
                target=target,
            )


class Assignment(sso.CfnAssignment):
    """L2 construct for SSO Assignment"""

    def __init__(
        self,
        scope: Construct,
        id: str,
        sso_instance: SsoInstance,
        permission_set: PermissionSet,
        principal: Principal,
        target: Target,
    ) -> None:
        super().__init__(
            scope=scope,
            id=f"{id}Assignment",
            instance_arn=sso_instance.sso_instance_arn,
            permission_set_arn=permission_set.permission_set_arn,
            principal_id=principal.principal_id,
            principal_type=principal.principal_type,
            target_id=target.target_id,
            target_type=target.target_type,
        )
