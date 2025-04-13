import enum
from typing import Self

import pydantic


class ColumnType(enum.Enum):
    NUMBER = enum.auto()
    BOOLEAN = enum.auto()


HabitValue = int | float | bool


class ColumnDetails(pydantic.BaseModel):
    key: str
    column_type: ColumnType
    display_name: str
    column_reference: str | None = None

    @classmethod
    def from_yaml(cls, details: dict[str, str], key: str) -> Self:
        """
        Create a ColumnDetails object from YAML details.
        """
        return cls(
            key=key,
            column_type=ColumnType[details["column_type"].upper()],
            display_name=details["display_name"],
            column_reference=details.get("column_reference"),
        )

    def check_value_type_matches(self, value: HabitValue) -> bool:
        """
        Checks a value matches the column type.
        """
        if self.column_type == ColumnType.NUMBER:
            return isinstance(value, (int, float)) and not isinstance(value, bool)
        elif self.column_type == ColumnType.BOOLEAN:
            return isinstance(value, bool)
        else:
            raise ValueError(f"Unknown column type: {self.column_type}")
