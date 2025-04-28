"""
This module contains tests for the models in the resources package
"""
import pytest
from tests.utils import create_units_complete_export


class TestUnitsCompleteExport:
    """
    Test class for UnitsCompleteExport model.
    """

    @pytest.fixture(scope="function")
    def valid_export(self):
        """
        Fixture to create a valid UnitsCompleteExport instance.
        """
        return create_units_complete_export()

    def test_units_complete_export_with_valid_attributes(self, valid_export):
        """
        Test that a UnitsCompleteExport record can be created with valid attributes.
        """
        export = valid_export
        assert export.export_id == 1
        assert export.job_number == "123456"
        assert export.job_date == "2023-10-01"
        assert export.phase_number == "Phase"
        assert export.category_number == "Category"
        assert export.unit_change == 100
        assert export.timesheet_id == 1
        assert export.change_order_id == 1
        assert export.sub_report_id == 1
        assert export.vendor_name == "Vendor"
        assert export.date_created == "2023-10-01 00:00:00"

    def test_units_complete_export_to_dict(self, valid_export):
        """
        Test that the to_dict method returns the correct dictionary representation.
        """
        export = valid_export
        expected_dict = {
            "job_date": "2023-10-01",
            "job_number": "123456",
            "phase_number": "Phase",
            "category_number": "Category",
            "missing_from_budget": None,
            "unit_change": 100,
            "notes": export.get_notes(),
            "cost_code": export.get_cost_code(),
        }
        assert export.to_dict() == expected_dict

    def test_units_complete_export_repr(self, valid_export):
        """
        Test that the __repr__ method returns the correct string representation.
        """
        export = valid_export
        expected_repr = (f"<UnitsCompleteExport(export_id={export.export_id}, "
                         f"job_number={export.job_number}, "
                         f"job_date={export.job_date}, "
                         f"phase_number={export.phase_number}, "
                         f"category_number={export.category_number}, "
                         f"unit_change={export.unit_change}, "
                         f"timesheet_id={export.timesheet_id}, "
                         f"change_order_id={export.change_order_id}, "
                         f"sub_report_id={export.sub_report_id}, "
                         f"vendor_name={export.vendor_name}, "
                         f"date_created={export.date_created})>")
        assert repr(export) == expected_repr
