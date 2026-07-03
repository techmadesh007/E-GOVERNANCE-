"""User authentication.

Passwords are never stored in plain text: each one is salted and hashed
with SHA-256 before being written to disk. ENCAPSULATION hides those
hashing details behind a small public register()/login() interface.
"""
import hashlib
import secrets
from abc import ABC, abstractmethod


class AuthProvider(ABC):
    """ABSTRACTION: any authentication backend must support these two ops."""

    @abstractmethod
    def register(self, username: str, password: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def login(self, username: str, password: str) -> bool:
        raise NotImplementedError


class FileAuthProvider(AuthProvider):
    """INHERITANCE: stores salted password hashes in a local text file.
    POLYMORPHISM: implements register()/login() its own way; a future
    DatabaseAuthProvider could implement them completely differently
    without AuthenticationService (below) ever needing to change."""

    def __init__(self, filepath: str = "users.txt"):
        self._filepath = filepath          # ENCAPSULATION: private state
        self._users = self.__load_users()  # name-mangled: truly private

    def __load_users(self) -> dict:
        users = {}
        try:
            with open(self._filepath, "r") as file:
                for line in file:
                    parts = line.strip().split(":")
                    if len(parts) == 3:
                        username, salt, hashed = parts
                        users[username] = (salt, hashed)
        except FileNotFoundError:
            pass  # No users registered yet -- start with an empty table.
        return users

    @staticmethod
    def __hash_password(password: str, salt: str) -> str:
        return hashlib.sha256((salt + password).encode("utf-8")).hexdigest()

    def register(self, username: str, password: str) -> bool:
        if not username or not password or username in self._users:
            return False

        salt = secrets.token_hex(8)
        hashed = self.__hash_password(password, salt)
        self._users[username] = (salt, hashed)

        with open(self._filepath, "a") as file:
            file.write(f"{username}:{salt}:{hashed}\n")
        return True

    def login(self, username: str, password: str) -> bool:
        if username not in self._users:
            return False
        salt, stored_hash = self._users[username]
        return self.__hash_password(password, salt) == stored_hash


class AuthenticationService:
    """Front-facing service used by the console app. Depends only on the
    abstract AuthProvider interface, so any provider can be swapped in."""

    def __init__(self, provider: AuthProvider = None):
        self._provider = provider or FileAuthProvider()

    def sign_up(self, username: str, password: str) -> bool:
        return self._provider.register(username, password)

    def sign_in(self, username: str, password: str) -> bool:
        return self._provider.login(username, password)