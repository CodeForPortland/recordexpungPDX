import unittest

from datetime import datetime, timedelta

from expungeservice.models.expungement_result import EligibilityStatus
from expungeservice.models.charge_types.misdemeanor import Misdemeanor
from expungeservice.models.disposition import Disposition

from tests.factories.charge_factory import ChargeFactory
from tests.models.test_charge import ChargeTypeTest


class TestSingleChargeConvictionsMisdemeanor(ChargeTypeTest):
    def setUp(self):
        super().setUp()
        self.charge_dict["disposition"] = self.convicted

    def test_misdemeanor(self):
        self.charge_dict["name"] = "Criminal Trespass in the Second Degree"
        self.charge_dict["statute"] = "164.245"
        self.charge_dict["level"] = "Misdemeanor Class C"
        self.charge_dict["disposition"] = None

        misdemeanor_charge = self.create_recent_charge()
        self.charges.append(misdemeanor_charge)

        assert isinstance(misdemeanor_charge, Misdemeanor)
        assert misdemeanor_charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert (
            misdemeanor_charge.expungement_result.type_eligibility.reason
            == "Misdemeanors are always eligible under 137.225(5)(b) for convictions, or 137.225(1)(b) for dismissals"
        )

    def test_misdemeanor_164043(self):
        self.charge_dict["name"] = "Theft in the third degree"
        self.charge_dict["statute"] = "164.043"
        self.charge_dict["level"] = "Misdemeanor Class C"
        charge = self.create_recent_charge()
        self.charges.append(charge)

        assert isinstance(charge, Misdemeanor)
        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(b)"

    def test_misdemeanor_164125(self):
        self.charge_dict["name"] = "Theft of services"
        self.charge_dict["statute"] = "164.125"
        self.charge_dict["level"] = "Misdemeanor Class A"
        charge = self.create_recent_charge()
        self.charges.append(charge)

        assert isinstance(charge, Misdemeanor)
        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(b)"

    def test_drug_free_zone_variance_misdemeanor(self):
        self.charge_dict["name"] = "	Drug Free Zone Variance"
        self.charge_dict["statute"] = "14B20060"
        self.charge_dict["level"] = "Misdemeanor Unclassified"
        charge = self.create_recent_charge()
        self.charges.append(charge)

        assert isinstance(charge, Misdemeanor)
        assert charge.expungement_result.type_eligibility.status is EligibilityStatus.ELIGIBLE
        assert charge.expungement_result.type_eligibility.reason == "Eligible under 137.225(5)(b)"