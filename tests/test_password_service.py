"""Tests du service de gestion des mots de passe."""

from kampusbank.service.password_service import (
    hacher_mot_de_passe,
    verifier_mot_de_passe,
)


def test_hachage_different_du_mot_de_passe() -> None:
    mot_de_passe = "Kampus123"

    resultat = hacher_mot_de_passe(mot_de_passe)

    assert resultat != mot_de_passe


def test_verification_mot_de_passe_correct() -> None:
    mot_de_passe = "Kampus123"
    mot_de_passe_hash = hacher_mot_de_passe(mot_de_passe)

    resultat = verifier_mot_de_passe(
        mot_de_passe,
        mot_de_passe_hash,
    )

    assert resultat is True


def test_verification_mot_de_passe_incorrect() -> None:
    mot_de_passe_hash = hacher_mot_de_passe("Kampus123")

    resultat = verifier_mot_de_passe(
        "MauvaisMotDePasse123",
        mot_de_passe_hash,
    )

    assert resultat is False


def test_deux_hachages_sont_differents() -> None:
    mot_de_passe = "Kampus123"

    premier_hash = hacher_mot_de_passe(mot_de_passe)
    deuxieme_hash = hacher_mot_de_passe(mot_de_passe)

    assert premier_hash != deuxieme_hash