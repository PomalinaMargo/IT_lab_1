import unittest
from core.database import Database
from core.table import Table
from core.row import Row
from core.column import Column, IntegerColumn, TextColumn


class DatabaseTest(unittest.TestCase):
    def test_create_db_success(self):
        db = Database("test_db")
        self.assertEqual(db.tables, [])
        self.assertEqual(db.name, "test_db")

    def test_create_db_fail(self):
        with self.assertRaises(Exception):
            Database(1)

        with self.assertRaises(Exception):
            Database()


class TableTest(unittest.TestCase):
    def test_create_table_success(self):
        table = Table("test_table")
        self.assertEqual(table.rows, [])
        self.assertEqual(table.name, "test_table")
        self.assertEqual(table.columns, [])

    def test_create_table_fail(self):
        with self.assertRaises(Exception):
            Table(1)

        with self.assertRaises(Exception):
            Table()

    def test_add_column_success(self):
        table = Table("test_table")
        table.add_column(IntegerColumn("id"))
        table.add_column(TextColumn("name"))

        self.assertEqual(len(table.columns), 2)
        self.assertEqual(table.columns[0].name, "id")
        self.assertEqual(table.columns[1].name, "name")

    def test_add_column_fail(self):
        table = Table("test_table")

        with self.assertRaises(Exception):
            table.add_column(IntegerColumn("id"))
            table.add_column(TextColumn("id"))

        with self.assertRaises(Exception):
            table.add_column(1)


class ColumnTest(unittest.TestCase):
    def test_create_column_success(self):
        column = Column("test_column")
        self.assertEqual(column.name, "test_column")
        self.assertEqual(column.type, None)

    def test_create_column_fail(self):
        with self.assertRaises(Exception):
            Column(1)

        with self.assertRaises(Exception):
            Column()


class IntegerColumnTest(unittest.TestCase):
    def test_create_column_success(self):
        column = IntegerColumn("test_column")
        self.assertEqual(column.name, "test_column")
        self.assertEqual(column.type, "int")

    def test_create_column_fail(self):
        with self.assertRaises(Exception):
            IntegerColumn(1)

        with self.assertRaises(Exception):
            IntegerColumn()

    def test_validate_success(self):
        column = IntegerColumn("test_column")
        self.assertTrue(column.validate(1))
        self.assertTrue(column.validate(0))
        self.assertTrue(column.validate(-1))

    def test_validate_fail(self):
        column = IntegerColumn("test_column")
        self.assertFalse(column.validate(1.0))
        self.assertFalse(column.validate(0.0))
        self.assertFalse(column.validate(-1.0))
        self.assertFalse(column.validate("1.0"))
        self.assertFalse(column.validate("0.0"))
        self.assertFalse(column.validate("-1.0"))


class JoinTablesTest(unittest.TestCase):
    def setUp(self):
        self.db = Database("shop")

        self.products = Table("Products")
        self.products.add_column(IntegerColumn("ProductId"))
        self.products.add_column(TextColumn("Name"))
        self.products.add_row(Row(self.products, [1, "Bread"]))
        self.products.add_row(Row(self.products, [2, "Milk"]))
        self.products.add_row(Row(self.products, [3, "Cheese"]))

        self.sales = Table("Sales")
        self.sales.add_column(IntegerColumn("ProductId"))
        self.sales.add_column(IntegerColumn("Qty"))
        self.sales.add_row(Row(self.sales, [1, 3]))
        self.sales.add_row(Row(self.sales, [2, 1]))
        self.sales.add_row(Row(self.sales, [4, 10]))

        self.db.add_table(self.products)
        self.db.add_table(self.sales)

    def test_join_success(self):
        joined = self.db.join_tables("Products", "Sales", "ProductId")

        self.assertTrue(joined.name.startswith("Products_Sales"))

        joined_col_names = [c.name for c in joined.columns]
        self.assertIn("Products.ProductId", joined_col_names)
        self.assertIn("Products.Name", joined_col_names)
        self.assertIn("Sales.Qty", joined_col_names)
        self.assertNotIn("Sales.ProductId", joined_col_names)

        self.assertEqual(len(joined.rows), 2)

        idx_prod_id = joined_col_names.index("Products.ProductId")
        idx_name = joined_col_names.index("Products.Name")
        idx_qty = joined_col_names.index("Sales.Qty")

        got = sorted([(r.values[idx_prod_id], r.values[idx_name], r.values[idx_qty]) for r in joined.rows])
        self.assertEqual(got, [(1, "Bread", 3), (2, "Milk", 1)])

    def test_join_no_matches(self):
        sales2 = Table("Sales2")
        sales2.add_column(IntegerColumn("ProductId"))
        sales2.add_column(IntegerColumn("Qty"))
        sales2.add_row(Row(sales2, [10, 1]))
        sales2.add_row(Row(sales2, [20, 2]))
        self.db.add_table(sales2)

        joined = self.db.join_tables("Products", "Sales2", "ProductId")
        self.assertEqual(len(joined.rows), 0)
        joined_col_names = [c.name for c in joined.columns]
        self.assertIn("Products.ProductId", joined_col_names)
        self.assertIn("Sales2.Qty", joined_col_names)

    def test_join_missing_field_left(self):
        t = Table("NoKeyLeft")
        t.add_column(TextColumn("Name"))
        self.db.add_table(t)

        with self.assertRaises(ValueError):
            self.db.join_tables("NoKeyLeft", "Sales", "ProductId")

    def test_join_missing_field_right(self):
        t = Table("NoKeyRight")
        t.add_column(TextColumn("Name"))
        self.db.add_table(t)

        with self.assertRaises(ValueError):
            self.db.join_tables("Products", "NoKeyRight", "ProductId")

if __name__ == '__main__':
    unittest.main()
