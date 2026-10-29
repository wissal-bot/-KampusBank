"""Service d'authentification des utilisateurs de KampusBank."""

from datetime import datetime, timedelta

from kampusbank.domaine.exceptions import (
    AuthentificationError,
    UtilisateurBloqueError,
)
from kampusbank.domaine.user import User
from kampusbank.persistance.user_repository import UserRepository
from kampusbank.service.password_service import verifier_mot_de_passe


class AuthentificationService:
    """Gère l'authentification et les tentatives de connexion."""

    MAX_TENTATIVES = 5
    DUREE_BLOCAGE_MINUTES = 15

    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    def connecter(
        self,
        email: str,
        mot_de_passe: str,
        maintenant: datetime | None = None,
    ) -> User:
        """Authentifie un utilisateur."""

        if maintenant is None:
            maintenant = datetime.now()

        user = self._user_repository.trouver_par_email(email)

        if user is None:
            raise AuthentificationError(
                "Adresse e-mail ou mot de passe incorrect."
            )

        if (
            user.bloque_jusqu_a is not None
            and maintenant < user.bloque_jusqu_a
        ):
            raise UtilisateurBloqueError(
                "Le compte est temporairement bloqué."
            )

        if (
            user.bloque_jusqu_a is not None
            and maintenant >= user.bloque_jusqu_a
        ):
            user.bloque_jusqu_a = None
            user.tentatives_connexion = 0

        if not verifier_mot_de_passe(
            mot_de_passe,
            user.mot_de_passe_hash,
        ):
            user.tentatives_connexion += 1

            if user.tentatives_connexion >= self.MAX_TENTATIVES:
                user.bloque_jusqu_a = maintenant + timedelta(
                    minutes=self.DUREE_BLOCAGE_MINUTES
                )

                raise UtilisateurBloqueError(
                    "Trop de tentatives. Compte bloqué pendant 15 minutes."
                )

            raise AuthentificationError(
                "Adresse e-mail ou mot de passe incorrect."
            )

        user.tentatives_connexion = 0
        user.bloque_jusqu_a = None

        return user