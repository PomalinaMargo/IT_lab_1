from typing import List
from core.column import Column
from core.row import Row

class Table:
    def __init__(self, name: str):
        assert isinstance(name, str), "name must be a string"

        self.name = name
        self.columns: List[Column] = []
        self.rows: List[Row] = []

    def add_column(self, column: Column):
        if not isinstance(column, Column):
            raise TypeError("column must be an instance of Column")

        for column_ in self.columns:
            if column_.name == column.name:
                raise ValueError("column with this name already exists")

        self.columns.append(column)

        for row in self.rows:
            row.values.append(None)

    def del_column(self, column_name: str):
        for i, column in enumerate(self.columns):
            if column.name == column_name:
                self.columns.remove(column)
                for row in self.rows:
                    row.values.pop(i)
                return
        raise ValueError(f"column {column_name} not found")

    def add_row(self, row):
        if not isinstance(row, Row):
            raise TypeError("row must be an instance of Row")

        for col, val in zip(self.columns, row.values):
            if not col.validate(val):
                raise ValueError(f"column {col.name} does not accept value {val}")

        for row_ in self.rows:
            if row_.id == row.id:
                raise ValueError("row with this id already exists")

        self.rows.append(row)

    def to_json(self):
        return {
            "name": self.name,
            "columns": [{"name": col.name, "type": col.type} for col in self.columns],
            "rows": [[str(val) for val in row.values] for row in self.rows]
        }
