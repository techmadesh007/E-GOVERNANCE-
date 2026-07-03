"""Polymorphic eligibility rule hierarchy.

Each concrete Rule subclass encapsulates ONE eligibility criterion and
overrides is_violated() / failure_message() (POLYMORPHISM). The abstract
base class Rule (ABSTRACTION, via ABC) guarantees every rule exposes the
same interface, so EligibilityChecker never needs to know which concrete
rule type it is dealing with -- it just calls rule.is_violated(citizen).
"""
from abc import ABC, abstractmethod


class Rule(ABC):
    """Abstract base class for a single eligibility criterion."""

    def __init__(self, expected_value):
        self._expected_value = expected_value  # ENCAPSULATION: hidden state

    @property
    def expected_value(self):
        """Read-only access to the configured rule value."""
        return self._expected_value

    @abstractmethod
    def is_violated(self, citizen: dict) -> bool:
        """Return True if the citizen breaks this rule."""
        raise NotImplementedError

    @abstractmethod
    def failure_message(self) -> str:
        """Human readable reason the citizen failed this rule."""
        raise NotImplementedError


class OccupationRule(Rule):
    """INHERITANCE: extends Rule. POLYMORPHISM: own implementation below."""

    def is_violated(self, citizen: dict) -> bool:
        return citizen["occupation"].lower() != str(self.expected_value).lower()

    def failure_message(self) -> str:
        return f"Only {self.expected_value}s can apply"


class GenderRule(Rule):
    def is_violated(self, citizen: dict) -> bool:
        return citizen["gender"].lower() != str(self.expected_value).lower()

    def failure_message(self) -> str:
        return f"This scheme is only for {self.expected_value} applicants"


class IncomeRule(Rule):
    def is_violated(self, citizen: dict) -> bool:
        return citizen["income"] > self.expected_value

    def failure_message(self) -> str:
        return "Income exceeds limit"


class MinAgeRule(Rule):
    def is_violated(self, citizen: dict) -> bool:
        return citizen["age"] < self.expected_value

    def failure_message(self) -> str:
        return "Age below minimum limit"


class MaxAgeRule(Rule):
    def is_violated(self, citizen: dict) -> bool:
        return citizen["age"] > self.expected_value

    def failure_message(self) -> str:
        return "Age exceeds maximum limit"


# COLLECTIONS: dict used as a lookup table (factory) mapping a scheme's
# rule-dict key to the Rule subclass that enforces it.
RULE_FACTORY = {
    "occupation": OccupationRule,
    "gender": GenderRule,
    "income": IncomeRule,
    "min_age": MinAgeRule,
    "max_age": MaxAgeRule,
}
