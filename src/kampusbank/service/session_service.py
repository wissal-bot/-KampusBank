"""Service de gestion de la session utilisateur."""

from kampusbank.domaine.exceptions import AuthentificationError
from kampusbank.domaine.user import Role, User


class SessionService:
    """Gère l'utilisateur actuellement connecté."""

    def __init__(self) -> None:
        self._utilisateur_connecte: User | None = None

    @property
    def utilisateur_connecte(self) -> User | None:
        """Retourne l'utilisateur actuellement connecté."""
        return self._utilisateur_connecte

    def ouvrir_session(self, user: User) -> None:
        """Ouvre une session pour un utilisateur."""
        self._utilisateur_connecte = user

    def fermer_session(self) -> None:
        """Ferme la session actuelle."""
        self._utilisateur_connecte = None

    def exiger_utilisateur_connecte(self) -> User:
        """Retourne l'utilisateur connecté ou refuse l'accès."""
        if self._utilisateur_connecte is None:
            raise AuthentificationError(
                "Vous devez être connecté pour accéder à cette fonctionnalité."
            )

        return self._utilisateur_connecte

    def exiger_admin(self) -> User:
        """Vérifie que l'utilisateur connecté est administrateur."""
        user = self.exiger_utilisateur_connecte()

        if user.role != Role.ADMIN:
            raise AuthentificationError(
                "Cette fonctionnalité est réservée aux administrateurs."
            )

        return user