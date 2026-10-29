"""Tests du service de gestion de session."""

import pytest

from kampusbank.domaine.exceptions import AuthentificationError
from kampusbank.domaine.user import Role, User
from kampusbank.service.session_service import SessionService


def creer_user(role: Role = Role.CLIENT) -> User:
    """Crée un utilisateur pour les tests."""
    return User(
        id="123",
        nom="Kerkour",
        prenom="Wissal",
        email="wissal@example.com",
        telephone="0612345678",
        mot_de_passe_hash="hash-test",
        role=role,
    )


def test_aucun_utilisateur_connecte_au_depart() -> None:
    session = SessionService()

    assert session.utilisateur_connecte is None


def test_ouverture_session() -> None:
    session = SessionService()
    user = creer_user()

    session.ouvrir_session(user)

    assert session.utilisateur_connecte == user


def test_fermeture_session() -> None:
    session = SessionService()
    user = creer_user()

    session.ouvrir_session(user)
    session.fermer_session()

    assert session.utilisateur_connecte is None


def test_acces_refuse_sans_connexion() -> None:
    session = SessionService()

    with pytest.raises(AuthentificationError):
        session.exiger_utilisateur_connecte()


def test_client_refuse_sur_espace_admin() -> None:
    session = SessionService()
    client = creer_user(Role.CLIENT)

    session.ouvrir_session(client)

    with pytest.raises(AuthentificationError):
        session.exiger_admin()


def test_admin_autorise_sur_espace_admin() -> None:
    session = SessionService()
    admin = creer_user(Role.ADMIN)

    session.ouvrir_session(admin)

    resultat = session.exiger_admin()

    assert resultat == admin