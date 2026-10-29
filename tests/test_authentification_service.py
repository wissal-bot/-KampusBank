"""Tests du service d'authentification."""

from datetime import datetime, timedelta

import pytest

from kampusbank.domaine.exceptions import (
    AuthentificationError,
    UtilisateurBloqueError,
)
from kampusbank.persistance.user_repository import InMemoryUserRepository
from kampusbank.service.authentification_service import (
    AuthentificationService,
)
from kampusbank.service.inscription_service import InscriptionService


def preparer_services() -> tuple[
    InscriptionService,
    AuthentificationService,
]:
    repository = InMemoryUserRepository()

    inscription_service = InscriptionService(repository)
    authentification_service = AuthentificationService(repository)

    return inscription_service, authentification_service


def test_connexion_reussie() -> None:
    inscription, authentification = preparer_services()

    user = inscription.inscrire(
        nom="Kerkour",
        prenom="Wissal",
        email="wissal@example.com",
        telephone="0612345678",
        mot_de_passe="Kampus123",
    )

    user_connecte = authentification.connecter(
        "wissal@example.com",
        "Kampus123",
    )

    assert user_connecte == user


def test_connexion_email_inconnu() -> None:
    _, authentification = preparer_services()

    with pytest.raises(AuthentificationError):
        authentification.connecter(
            "inconnu@example.com",
            "Kampus123",
        )


def test_connexion_mauvais_mot_de_passe() -> None:
    inscription, authentification = preparer_services()

    inscription.inscrire(
        nom="Kerkour",
        prenom="Wissal",
        email="wissal@example.com",
        telephone="0612345678",
        mot_de_passe="Kampus123",
    )

    with pytest.raises(AuthentificationError):
        authentification.connecter(
            "wissal@example.com",
            "Mauvais123",
        )


def test_compte_bloque_apres_cinq_echecs() -> None:
    inscription, authentification = preparer_services()

    user = inscription.inscrire(
        nom="Kerkour",
        prenom="Wissal",
        email="wissal@example.com",
        telephone="0612345678",
        mot_de_passe="Kampus123",
    )

    maintenant = datetime(2026, 10, 29, 10, 0)

    for _ in range(4):
        with pytest.raises(AuthentificationError):
            authentification.connecter(
                "wissal@example.com",
                "Mauvais123",
                maintenant,
            )

    with pytest.raises(UtilisateurBloqueError):
        authentification.connecter(
            "wissal@example.com",
            "Mauvais123",
            maintenant,
        )

    assert user.tentatives_connexion == 5
    assert user.bloque_jusqu_a == maintenant + timedelta(minutes=15)


def test_connexion_refusee_pendant_blocage() -> None:
    inscription, authentification = preparer_services()

    inscription.inscrire(
        nom="Kerkour",
        prenom="Wissal",
        email="wissal@example.com",
        telephone="0612345678",
        mot_de_passe="Kampus123",
    )

    maintenant = datetime(2026, 10, 29, 10, 0)

    for _ in range(5):
        try:
            authentification.connecter(
                "wissal@example.com",
                "Mauvais123",
                maintenant,
            )
        except (AuthentificationError, UtilisateurBloqueError):
            pass

    with pytest.raises(UtilisateurBloqueError):
        authentification.connecter(
            "wissal@example.com",
            "Kampus123",
            maintenant + timedelta(minutes=10),
        )


def test_connexion_possible_apres_blocage() -> None:
    inscription, authentification = preparer_services()

    user = inscription.inscrire(
        nom="Kerkour",
        prenom="Wissal",
        email="wissal@example.com",
        telephone="0612345678",
        mot_de_passe="Kampus123",
    )

    maintenant = datetime(2026, 10, 29, 10, 0)

    for _ in range(5):
        try:
            authentification.connecter(
                "wissal@example.com",
                "Mauvais123",
                maintenant,
            )
        except (AuthentificationError, UtilisateurBloqueError):
            pass

    user_connecte = authentification.connecter(
        "wissal@example.com",
        "Kampus123",
        maintenant + timedelta(minutes=16),
    )

    assert user_connecte == user
    assert user.tentatives_connexion == 0
    assert user.bloque_jusqu_a is None