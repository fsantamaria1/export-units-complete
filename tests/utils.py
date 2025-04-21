"""
Utility functions for testing.
"""
from resources.models import UnitsCompleteExport


def create_units_complete_export(export_id=None):
    """
    Utility function to create a UnitsCompleteExport instance.
    """
    return UnitsCompleteExport(
        export_id=export_id or 1,
        job_number="123456",
        job_date="2023-10-01",
        phase_number="Phase",
        category_number="Category",
        unit_change=100,
        timesheet_id=1,
        change_order_id=1,
        sub_report_id=1,
        vendor_name="Vendor",
        date_created="2023-10-01 00:00:00",
    )
