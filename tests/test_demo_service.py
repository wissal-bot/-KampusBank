"""Tests du service de données de démonstration."""

from kampusbank.domaine.user import Role
from kampusbank.persistance.user_repository import InMemoryUserRepository
from kampusbank.service.demo_service import creer_admin_demo
from kampusbank.service.password_service import verifier_mot_de_passe


def test_creer_admin_demo() -> None:
    """Vérifie que l'administrateur de démonstration est créé."""
    repository = InMemoryUserRepository()

    creer_admin_demo(repository)

    admin = repository.trouver_par_email("admin@kampusbank.fr")

    assert admin is not None
    assert admin.prenom == "Admin"
    assert admin.nom == "KampusBank"
    assert admin.role == Role.ADMIN
    assert verifier_mot_de_passe(
        "Admin123",
        admin.mot_de_passe_hash,
    )


def test_admin_demo_ne_doit_pas_etre_cree_deux_fois() -> None:
    """Vérifie que l'administrateur n'est pas dupliqué."""
    repository = InMemoryUserRepository()

    creer_admin_demo(repository)
    premier_admin = repository.trouver_par_email(
        "admin@kampusbank.fr"
    )

    creer_admin_demo(repository)
    deuxieme_admin = repository.trouver_par_email(
        "admin@kampusbank.fr"
    )

    assert premier_admin is deuxieme_admin