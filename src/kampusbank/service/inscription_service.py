"""Service d'inscription des utilisateurs de KampusBank."""

from uuid import uuid4

from kampusbank.domaine.exceptions import EmailDejaUtiliseError
from kampusbank.domaine.user import Role, User
from kampusbank.domaine.validators import (
    valider_email,
    valider_mot_de_passe,
    valider_telephone,
)
from kampusbank.persistance.user_repository import UserRepository
from kampusbank.service.password_service import hacher_mot_de_passe


class InscriptionService:
    """Gère l'inscription des nouveaux clients."""

    def __init__(self, user_repository: UserRepository) -> None:
        self._user_repository = user_repository

    def inscrire(
        self,
        nom: str,
        prenom: str,
        email: str,
        telephone: str,
        mot_de_passe: str,
    ) -> User:
        """Inscrit un nouveau client dans KampusBank."""

        valider_email(email)
        valider_telephone(telephone)
        valider_mot_de_passe(mot_de_passe)

        if self._user_repository.trouver_par_email(email) is not None:
            raise EmailDejaUtiliseError(
                "Cette adresse e-mail est déjà utilisée."
            )

        user = User(
            id=str(uuid4()),
            nom=nom,
            prenom=prenom,
            email=email,
            telephone=telephone,
            mot_de_passe_hash=hacher_mot_de_passe(mot_de_passe),
            role=Role.CLIENT,
        )

        self._user_repository.ajouter(user)

        return user