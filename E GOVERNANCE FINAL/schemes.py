"""Scheme data and lookup.

Eligibility figures below are simplified, numeric criteria drawn from each
scheme's official/public guidelines (as of mid-2026) so they can be checked
by EligibilityChecker. Several real schemes also apply non-numeric
conditions (SECC data, caste certificates, state-wise rollout, document
verification, etc.) that this demo does not model. Always confirm on the
scheme's official portal (e.g. myscheme.gov.in) before relying on this data.
"""
from collections import OrderedDict

from repository import BaseRepository

# COLLECTIONS: OrderedDict makes the intentional display ordering explicit.
SCHEMES = OrderedDict([
    ("Agriculture", OrderedDict([
        ("PM Kisan", {"occupation": "Farmer"}),
        ("Kisan Credit Card", {"occupation": "Farmer"}),
        ("PM Fasal Bima Yojana", {"occupation": "Farmer"}),
    ])),

    ("Housing", OrderedDict([
        ("PM Awas Yojana", {"income": 500000}),
        ("Affordable Rental Housing Scheme", {"income": 400000}),
        ("Credit Linked Subsidy Scheme", {"income": 600000}),
    ])),

    ("Finance", OrderedDict([
        ("Atal Pension Yojana", {"min_age": 18, "max_age": 40}),
        ("Pradhan Mantri Jan Dhan Yojana", {"min_age": 18}),
        ("Pradhan Mantri Mudra Yojana", {"income": 800000}),
        # Immediate-annuity pension plan for senior citizens (LIC-operated).
        ("Pradhan Mantri Vaya Vandana Yojana", {"min_age": 60}),
    ])),

    ("Health", OrderedDict([
        # Since Sep 2024, all citizens 70+ qualify for PM-JAY cover
        # regardless of income.
        ("Ayushman Bharat PM-JAY (Senior Citizen)", {"min_age": 70}),
        # Low-cost accident insurance for savings account holders.
        ("Pradhan Mantri Suraksha Bima Yojana", {"min_age": 18, "max_age": 70}),
    ])),

    ("Employment & Skill Development", OrderedDict([
        # Support for traditional artisans/craftspeople (18 trades),
        # e.g. carpenters, blacksmiths, potters, goldsmiths, tailors.
        ("PM Vishwakarma Yojana", {"occupation": "Artisan", "min_age": 18}),
    ])),

    ("Women & Child Welfare", OrderedDict([
        # Maternity benefit for pregnant/lactating women (first child).
        ("Pradhan Mantri Matru Vandana Yojana", {"gender": "Female", "min_age": 19}),
    ])),

    ("Education", OrderedDict([
        # Scholarship for meritorious students from economically weaker
        # sections (real criteria is class 9-12 enrolment + marks; age
        # range below approximates typical class 9-12 students).
        ("National Means-cum-Merit Scholarship", {
            "income": 350000,
            "min_age": 13,
            "max_age": 20,
        }),
    ])),
])


class SchemeRepository(BaseRepository):
    """Read-only lookup over the scheme data. INHERITANCE: extends
    BaseRepository and (POLYMORPHISM) provides its own summary()."""

    def __init__(self, data: OrderedDict = None):
        self._data = data or SCHEMES               # ENCAPSULATION
        self._sector_cache = list(self._data.keys())  # optimization: build once

    def sectors(self) -> list[str]:
        return self._sector_cache

    def schemes_in(self, sector: str) -> list[str]:
        return list(self._data[sector].keys())

    def rules(self, sector: str, scheme: str) -> dict:
        return self._data[sector][scheme]

    def summary(self) -> str:
        return f"SchemeRepository -> {len(self._sector_cache)} sectors loaded"


# Kept for backward compatibility with code importing `schemes` directly.
schemes = SCHEMES
