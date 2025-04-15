"""
This module contains integration tests for the database models
"""
import pytest
from sqlalchemy.exc import IntegrityError
from resources.models import UnitsCompleteExport


class TestUnitsCompleteExport:
    """
    Integration tests for the UnitsCompleteExport model.
    """

    def test_export_valid(
            self,
            db_session,
            valid_units_complete_export: UnitsCompleteExport):
        """
        Test that a UnitsCompleteExport record can be created with valid attributes.
        """

        db_session.add(valid_units_complete_export)
        db_session.flush()
        units_complete_export = db_session.query(UnitsCompleteExport).filter(
            UnitsCompleteExport.export_id == valid_units_complete_export.export_id
        ).first()

        assert units_complete_export.export_id == valid_units_complete_export.export_id
        assert units_complete_export.job_number == valid_units_complete_export.job_number
        assert units_complete_export.job_date == valid_units_complete_export.job_date
        assert units_complete_export.phase_number == valid_units_complete_export.phase_number
        assert units_complete_export.category_number == valid_units_complete_export.category_number
        assert units_complete_export.unit_change == valid_units_complete_export.unit_change
        assert units_complete_export.timesheet_id == valid_units_complete_export.timesheet_id
        assert units_complete_export.change_order_id == valid_units_complete_export.change_order_id
        assert units_complete_export.sub_report_id == valid_units_complete_export.sub_report_id
        assert units_complete_export.vendor_name == valid_units_complete_export.vendor_name
        assert units_complete_export.date_created == valid_units_complete_export.date_created

    @pytest.mark.parametrize(
        "valid_field_name, invalid_value",
        [
            ("job_number", None),
            ("job_date", None),
            ("phase_number", None),
            ("category_number", None),
            ("unit_change", None),
        ],
    )
    def test_export_with_null_non_nullables(
            self,
            db_session,
            valid_units_complete_export: UnitsCompleteExport,
            valid_field_name,
            invalid_value):
        """
        Test that a UnitsCompleteExport record cannot be created with invalid attributes.
        """
        setattr(valid_units_complete_export, valid_field_name, invalid_value)
        db_session.add(valid_units_complete_export)

        with pytest.raises(IntegrityError):
            db_session.flush()
