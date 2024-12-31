from constructs import Construct
from infra.constructs.l2.orgs import FeatureSet
from infra.constructs.l2.orgs import L2Organization


class B2Organization(Construct):
    """AWS Organizations resources"""

    def __init__(self, scope: Construct, id: str) -> None:
        super().__init__(scope, id)

        # Create the root of the organization
        self.organization = L2Organization(
            scope=self,
            id="Organization",
            feature_set=FeatureSet.ALL,
        )

        # Create organizational units
        higher_env_ou = self.organization.add_organizational_unit(name="HigherEnv")
        lower_env_ou = self.organization.add_organizational_unit(name="LowerEnv")

        # Create accounts
        self.prod_account = higher_env_ou.add_account(
            name="Production",
            email="admin+prod@real-life-iac.com",
        )
        self.sandbox_account = lower_env_ou.add_account(
            name="Sandbox",
            email="admin+sandbox@real-life-iac.com",
        )
        self.staging_account = lower_env_ou.add_account(
            name="Staging",
            email="admin+staging@real-life-iac.com",
        )
