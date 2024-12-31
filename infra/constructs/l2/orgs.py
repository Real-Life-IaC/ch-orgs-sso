from enum import StrEnum
from typing import Union

from aws_cdk import aws_organizations as orgs
from constructs import Construct


class L2Account(orgs.CfnAccount):
    """AWS Account"""

    def __init__(
        self,
        scope: Construct,
        id: str,
        name: str,
        email: str,
        parent: Union["L2OrganizationalUnit", "L2Organization"],
    ) -> None:
        super().__init__(
            scope=scope,
            id=id,
            account_name=name,
            email=email,
            parent_ids=[parent._id],  # type: ignore
        )

        self.id = id
        self.name = name
        self.email = email
        self.parent = parent

        self.account_id = self.attr_account_id
        self.account_arn = self.attr_arn
        self.account_status = self.attr_status
        self._id = self.attr_account_id


class L2OrganizationalUnit(orgs.CfnOrganizationalUnit):
    """AWS Organizational Unit"""

    def __init__(
        self,
        scope: Construct,
        id: str,
        name: str,
        parent: Union["L2OrganizationalUnit", "L2Organization"],
    ) -> None:
        super().__init__(
            scope=scope,
            id=id,
            name=name,
            parent_id=parent._id,  # type: ignore
        )

        self.id = id
        self.scope = scope
        self.name = name
        self.parent = parent

        self.organizational_unit_id = self.attr_id
        self.organizational_unit_arn = self.attr_arn
        self._id = self.attr_id

        self.accounts: dict[str, L2Account] = {}

    def add_account(self, name: str, email: str) -> L2Account:
        """Add an account to the organization"""

        self.accounts[name] = L2Account(
            scope=self.scope,
            id=name,
            name=name,
            email=email,
            parent=self,
        )
        return self.accounts[name]


class FeatureSet(StrEnum):
    """Feature Set for AWS Organizations"""

    ALL = "ALL"
    CONSOLIDATED_BILLING = "CONSOLIDATED_BILLING"


class L2Organization(orgs.CfnOrganization):
    """AWS Organization"""

    def __init__(
        self,
        scope: Construct,
        id: str,
        feature_set: FeatureSet,
    ) -> None:
        super().__init__(
            scope=scope,
            id=id,
            feature_set=feature_set,
        )
        self.id = id
        self.scope = scope

        self.organization_id = self.attr_id
        self.organization_arn = self.attr_arn
        self.account_id = self.attr_management_account_id
        self.account_arn = self.attr_management_account_arn
        self.account_email = self.attr_management_account_email
        self.root_id = self.attr_root_id
        self._id = self.attr_root_id

        self.organizational_units: dict[str, L2OrganizationalUnit] = {}
        self.accounts: dict[str, L2Account] = {}

    def add_organizational_unit(self, name: str) -> L2OrganizationalUnit:
        """Add an organizational unit to the organization"""

        self.organizational_units[name] = L2OrganizationalUnit(
            scope=self.scope,
            id=name,
            name=name,
            parent=self,
        )
        return self.organizational_units[name]

    def add_account(self, name: str, email: str) -> L2Account:
        """Add an account to the organization"""

        self.accounts[name] = L2Account(
            scope=self.scope,
            id=name,
            name=name,
            email=email,
            parent=self,
        )
        return self.accounts[name]
