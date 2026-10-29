"""Création des données de démonstration de KampusBank."""

from uuid import uuid4

from kampusbank.domaine.user import Role, User
from kampusbank.persistance.user_repository import UserRepository
from kampusbank.service.password_service import hacher_mot_de_passe


def creer_admin_demo(
    user_repository: UserRepository,
) -> None:
    """Crée l'administrateur de démonstration s'il n'existe pas."""

    email = "admin@kampusbank.fr"

    if user_repository.trouver_par_email(email) is not None:
        return

    admin = User(
        id=str(uuid4()),
        nom="KampusBank",
        prenom="Admin",
        email=email,
        telephone="0102030405",
        mot_de_passe_hash=hacher_mot_de_passe("Admin123"),
        role=Role.ADMIN,
    )

    user_repository.ajouter(admin)