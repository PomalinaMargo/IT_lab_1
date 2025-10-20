from typing import List
from core.table import Table
from core.column import Column
from core.row import Row

class Database:
    def __init__(self, name: str):
        assert isinstance(name, str), "name must be a string"

        self.name = name
        self.tables: List[Table] = []

    def get_table(self, table_name: str):
        for table in self.tables:
            if table.name == table_name:
                return table
        raise ValueError(f"table {table_name} not found")

    def add_table(self, table: Table):
        if not isinstance(table, Table):
            raise TypeError("table must be an instance of Table")

        for table_ in self.tables:
            if table_.name == table.name:
                raise ValueError("table with this name already exists")

        self.tables.append(table)

    def list_tables(self):
        return [table.name for table in self.tables]

    def del_table(self, table_name: str):
        for table in self.tables:
            if table.name == table_name:
                self.tables.remove(table)
                return
        raise ValueError(f"table {table_name} not found")

    def to_json(self):
        return {
            "name": self.name,
            "tables": [table.to_json() for table in self.tables]
        }
    
    def join_tables(self, table1_name: str, table2_name: str, on_field: str):
        """Join two tables by common field (inner join)."""
        table1 = self.get_table(table1_name)
        table2 = self.get_table(table2_name)

        try:
            idx1 = next(i for i, c in enumerate(table1.columns) if c.name == on_field)
            idx2 = next(i for i, c in enumerate(table2.columns) if c.name == on_field)
        except StopIteration:
            raise ValueError(f"Field '{on_field}' not found in one of the tables")

        joined_table = Table(f"{table1_name}_{table2_name}_join")

        for col in table1.columns:
            joined_table.add_column(Column.create_type_column(col.type, f"{table1.name}.{col.name}"))
        for col in table2.columns:
            if col.name != on_field:
                joined_table.add_column(Column.create_type_column(col.type, f"{table2.name}.{col.name}"))

        for row1 in table1.rows:
            for row2 in table2.rows:
                if row1.values[idx1] == row2.values[idx2]:
                    new_values = row1.values + [v for i, v in enumerate(row2.values) if i != idx2]
                    joined_table.add_row(Row(joined_table, new_values))

        return joined_table

