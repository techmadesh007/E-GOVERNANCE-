"""Eligibility checking logic.

Rule types supported in a scheme's rule dict:
    occupation : str   -> applicant's occupation must match (case-insensitive)
    gender     : str   -> applicant's gender must match (case-insensitive)
    income     : int   -> applicant's annual income must not exceed this
    min_age    : int   -> applicant's age must not be below this
    max_age    : int   -> applicant's age must not be above this

The actual rule checking is delegated to the polymorphic Rule hierarchy
in rules.py; this module just orchestrates which rules to run.
"""
from collections import namedtuple

from rules import RULE_FACTORY

# COLLECTIONS: namedtuple gives the citizen's data a clear, immutable shape
# instead of a loosely-typed dict passed around by hand.
Citizen = namedtuple("Citizen", ["age", "income", "occupation", "gender"])


class EligibilityChecker:
    """Checks a citizen's eligibility against a scheme's rule set."""

    @classmethod
    def check(cls, rules: dict, age: int, income: int, occupation: str, gender: str = "") -> tuple[bool, str]:
        """Returns (is_eligible, message) for the given citizen and rules."""
        try:
            citizen = Citizen(age=age, income=income, occupation=occupation, gender=gender)._asdict()

            for rule_key, rule_value in rules.items():
                rule = RULE_FACTORY[rule_key](rule_value)  # POLYMORPHISM
                if rule.is_violated(citizen):
                    return False, rule.failure_message()

            return True, "Eligible"

        except (TypeError, AttributeError, ValueError, KeyError):
            return False, "Invalid citizen data provided"


def check_eligibility(rules, age, income, occupation, gender=""):
    """Functional wrapper kept for backward compatibility."""
    return EligibilityChecker.check(rules, age, income, occupation, gender)
