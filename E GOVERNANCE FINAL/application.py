"""Application record persistence."""
from collections import Counter
from dataclasses import dataclass, astuple

from repository import BaseRepository


@dataclass
class ApplicationRecord:
    """A single scheme application made by a citizen."""
    name: str
    sector: str
    scheme: str
    status: str = "Applied"


class ApplicationRepository(BaseRepository):
    """Handles writing application records to disk. INHERITANCE: extends
    BaseRepository and (POLYMORPHISM) provides its own summary()."""

    def __init__(self, filepath: str = "applications.txt"):
        self._filepath = filepath          # ENCAPSULATION: private state
        self._status_counts = Counter()    # COLLECTIONS: tally by status

    @property
    def filepath(self) -> str:
        """Read-only access to the storage path."""
        return self._filepath

    def save(self, record: ApplicationRecord) -> None:
        with open(self._filepath, "a") as file:
            file.write(str(astuple(record)))
            file.write("\n")
        self._status_counts[record.status] += 1

    def status_counts(self) -> Counter:
        """Return a copy of how many applications were saved, per status."""
        return self._status_counts.copy()

    def summary(self) -> str:
        total_saved = sum(self._status_counts.values())
        return f"ApplicationRepository -> {self._filepath} ({total_saved} saved this session)"


def save_application(record):
    """Functional wrapper kept for backward compatibility.

    Accepts either an ApplicationRecord or a plain tuple
    (name, sector, scheme, status).
    """
    if not isinstance(record, ApplicationRecord):
        record = ApplicationRecord(*record)
    ApplicationRepository().save(record)
