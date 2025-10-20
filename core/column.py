from datetime import date

class Column:
    def __init__(self, name: str):
        assert isinstance(name, str), "name must be a string"
        self.name = name
        self.type = None

    @staticmethod
    def create_type_column(type: str, name: str):
        assert isinstance(type, str), "type must be a string"
        assert isinstance(name, str), "name must be a string"

        if type == "int":
            return IntegerColumn(name)
        elif type == "float" or type == "double":
            return RealColumn(name)
        elif type == "str" or type == "text" or type == "string":
            return TextColumn(name)
        elif type == "char":
            return CharColumn(name)
        elif type == "date":
            return DateColumn(name)
        elif type == "dateInvl":
            return DateInvlColumn(name)
        else:
            raise ValueError(f"unknown type {type}")

    def validate(self, value):
        pass

class IntegerColumn(Column):
    def __init__(self, name):
        super().__init__(name)
        self.type = "int"

    def validate(self, value):
        if value is None:
            return True
        if isinstance(value, str):
            try:
                value = int(value)
            except ValueError:
                return False
        return isinstance(value, int)


class RealColumn(Column):
    def __init__(self, name):
        super().__init__(name)
        self.type = "float"

    def validate(self, value):
        if value is None:
            return True
        if isinstance(value, str):
            try:
                value = float(value)
            except ValueError:
                return False
        return isinstance(value, float)


class TextColumn(Column):
    def __init__(self, name):
        super().__init__(name)
        self.type = "str"

    def validate(self, value):
        if value is None:
            return True
        return isinstance(value, str)


class CharColumn(Column):
    def __init__(self, name):
        super().__init__(name)
        self.type = "char"

    def validate(self, value):
        if value is None:
            return True
        return isinstance(value, str) and len(value) == 1


class DateColumn(Column):
    def __init__(self, name):
        super().__init__(name)
        self.type = "date"

    def validate(self, value):
        if value is None:
            return True
        if isinstance(value, str):
            try:
                value = date.fromisoformat(value)
            except ValueError:
                return False
        return isinstance(value, date)


class DateInvlColumn(Column):
    def __init__(self, name):
        super().__init__(name)
        self.type = "dateInvl"

    def validate(self, value_str: str):
        if ".." in value_str:
            parts = value_str.split("..", 1)
        elif "," in value_str:
            parts = value_str.split(",", 1)
        else:
            return False
        a, b = parts[0].strip(), parts[1].strip()
        try:
            da = date.fromisoformat(a)
            db = date.fromisoformat(b)
        except ValueError:
            return False
        if da > db:
            return False
        return True