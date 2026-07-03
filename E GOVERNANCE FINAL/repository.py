"""Abstract base repository shared by all data-access classes."""
from abc import ABC, abstractmethod


class BaseRepository(ABC):
    """ABSTRACTION: defines the contract every repository must follow.

    Concrete repositories (SchemeRepository, ApplicationRepository) inherit
    from this class (INHERITANCE) and each provides its own implementation
    of summary() (POLYMORPHISM) -- callers can treat any repository the
    same way without knowing its concrete type.
    """

    @abstractmethod
    def summary(self) -> str:
        """Return a short, human-readable description of this repository."""
        raise NotImplementedError
