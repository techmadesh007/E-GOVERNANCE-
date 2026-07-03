"""Sector listing and display."""
from enum import Enum


class Sector(Enum):
    """All sectors offering central government schemes."""
    AGRICULTURE = "Agriculture"
    HOUSING = "Housing"
    FINANCE = "Finance"
    HEALTH = "Health"
    EMPLOYMENT = "Employment & Skill Development"
    WOMEN_CHILD = "Women & Child Welfare"
    EDUCATION = "Education"

    @classmethod
    def names(cls) -> list[str]:
        """All sector display names, in declaration order."""
        return [member.value for member in cls]


def display_sectors() -> list[str]:
    """Prints the numbered list of sectors and returns their names."""
    sector_names = Sector.names()

    print("\nAvailable Sectors")
    for index, name in enumerate(sector_names, start=1):
        print(index, ".", name)

    return sector_names
