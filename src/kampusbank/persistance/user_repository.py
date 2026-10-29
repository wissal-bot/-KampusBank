"""Contrat de persistance des utilisateurs de KampusBank."""

from abc import ABC, abstractmethod

from kampusbank.domaine.user import User


class UserRepository(ABC):
    """Définit les opérations de persistance des utilisateurs."""

    @abstractmethod
    def ajouter(self, user: User) -> None:
        """Ajoute un utilisateur."""

    @abstractmethod
    def trouver_par_email(self, email: str) -> User | None:
        """Recherche un utilisateur à partir de son adresse e-mail."""

class InMemoryUserRepository(UserRepository):
    """Stocke temporairement les utilisateurs en mémoire."""

    def __init__(self) -> None:
        self._users: list[User] = []

    def ajouter(self, user: User) -> None:
        """Ajoute un utilisateur en mémoire."""
        self._users.append(user)

    def trouver_par_email(self, email: str) -> User | None:
        """Recherche un utilisateur par son adresse e-mail."""
        for user in self._users:
            if user.email == email:
                return user

        return None