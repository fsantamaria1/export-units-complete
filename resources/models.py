"""
This module contains the models for the database.
"""
import os
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, VARCHAR, DATE, NVARCHAR, NUMERIC, DATETIME

Base = declarative_base()


class UnitsCompleteExport(Base):
    """
    A class that represents the UnitsCompleteExport table in the database.
    """
    __tablename__ = 'UnitsCompleteExport'
    __table_args__ = {'schema': os.environ.get('schema_name', 'dbo')}

    export_id = Column(Integer, primary_key=True)
    job_number = Column(VARCHAR(10), nullable=False)
    job_date = Column(DATE, nullable=False)
    phase_number = Column(NVARCHAR(5), nullable=False)
    category_number = Column(NVARCHAR(15), nullable=False)
    unit_change = Column(NUMERIC(8, 2), nullable=False)
    timesheet_id = Column(Integer, nullable=True)
    change_order_id = Column(Integer, nullable=True)
    sub_report_id = Column(Integer, nullable=True)
    vendor_name = Column(NVARCHAR(30), nullable=True)
    date_created = Column(DATETIME, nullable=True)
    in_closed_period = Column(Integer, nullable=True)
    missing_from_budget = Column(Integer, nullable=True)

    def to_dict(self):
        """
        Convert the UnitsCompleteExport object to a dictionary.
        :return: A dictionary representation of the UnitsCompleteExport object.
        """
        fields = ['job_date', 'job_number', 'phase_number', 'category_number',
                  'unit_change', 'in_closed_period', 'missing_from_budget']
        data = {field: getattr(self, field) for field in fields}
        data['notes'] = self.get_notes()
        data['cost_code'] = self.get_cost_code()

        return data

    def get_notes(self):
        """
        Returns the notes for the UnitsCompleteExport object.
        """
        notes = []
        if self.timesheet_id:
            notes.append(f"Timesheet ID: {self.timesheet_id}")
        if self.change_order_id:
            notes.append(f"Change Order ID: {self.change_order_id}")
        if self.sub_report_id:
            notes.append(f"Sub Report ID: {self.sub_report_id}")
        if self.vendor_name:
            notes.append(f"Vendor Name: {self.vendor_name}")
        return " ".join(notes)

    def get_cost_code(self):
        """
        Returns the cost code for the UnitsCompleteExport object.
        """
        return f"{self.job_number}.{self.phase_number}.{self.category_number}"

    def __repr__(self):
        """
        Return a string representation of the UnitsCompleteExport object.
        :return: A string representation of the UnitsCompleteExport object.
        """
        return (f"<UnitsCompleteExport(export_id={self.export_id}, "
                f"job_number={self.job_number}, "
                f"job_date={self.job_date}, "
                f"phase_number={self.phase_number}, "
                f"category_number={self.category_number}, "
                f"unit_change={self.unit_change}, "
                f"timesheet_id={self.timesheet_id}, "
                f"change_order_id={self.change_order_id}, "
                f"sub_report_id={self.sub_report_id}, "
                f"vendor_name={self.vendor_name}, "
                f"date_created={self.date_created})>")
