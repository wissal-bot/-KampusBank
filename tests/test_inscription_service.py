"""Tests du service d'inscription."""

import pytest

from kampusbank.domaine.exceptions import (
    EmailDejaUtiliseError,
    ValidationError,
)
from kampusbank.domaine.user import Role
from kampusbank.persistance.user_repository import InMemoryUserRepository
from kampusbank.service.inscription_service import InscriptionService
from kampusbank.service.password_service import verifier_mot_de_passe


def creer_service() -> InscriptionService:
    repository = InMemoryUserRepository()
    return InscriptionService(repository)


def test_inscription_client() -> None:
    service = creer_service()

    user = service.inscrire(
        nom="Kerkour",
        prenom="Wissal",
        email="wissal@example.com",
        telephone="0612345678",
        mot_de_passe="Kampus123",
    )

    assert user.nom == "Kerkour"
    assert user.prenom == "Wissal"
    assert user.email == "wissal@example.com"
    assert user.role == Role.CLIENT


def test_mot_de_passe_est_hache() -> None:
    service = creer_service()

    user = service.inscrire(
        nom="Kerkour",
        prenom="Wissal",
        email="wissal@example.com",
        telephone="0612345678",
        mot_de_passe="Kampus123",
    )

    assert user.mot_de_passe_hash != "Kampus123"
    assert verifier_mot_de_passe(
        "Kampus123",
        user.mot_de_passe_hash,
    )


def test_email_deja_utilise() -> None:
    service = creer_service()

    service.inscrire(
        nom="Kerkour",
        prenom="Wissal",
        email="wissal@example.com",
        telephone="0612345678",
        mot_de_passe="Kampus123",
    )

    with pytest.raises(EmailDejaUtiliseError):
        service.inscrire(
            nom="Dupont",
            prenom="Jean",
            email="wissal@example.com",
            telephone="0698765432",
            mot_de_passe="Banque123",
        )


def test_inscription_refuse_email_invalide() -> None:
    service = creer_service()

    with pytest.raises(ValidationError):
        service.inscrire(
            nom="Kerkour",
            prenom="Wissal",
            email="email-invalide",
            telephone="0612345678",
            mot_de_passe="Kampus123",
        )


def test_inscription_refuse_telephone_invalide() -> None:
    service = creer_service()

    with pytest.raises(ValidationError):
        service.inscrire(
            nom="Kerkour",
            prenom="Wissal",
            email="wissal@example.com",
            telephone="123",
            mot_de_passe="Kampus123",
        )


def test_inscription_refuse_mot_de_passe_invalide() -> None:
    service = creer_service()

    with pytest.raises(ValidationError):
        service.inscrire(
            nom="Kerkour",
            prenom="Wissal",
            email="wissal@example.com",
            telephone="0612345678",
            mot_de_passe="bonjour",
        )