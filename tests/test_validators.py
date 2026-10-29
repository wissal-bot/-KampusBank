"""Tests des validateurs métier de KampusBank."""

import pytest

from kampusbank.domaine.exceptions import ValidationError
from kampusbank.domaine.validators import (
    valider_email,
    valider_mot_de_passe,
    valider_telephone,
)


def test_email_valide() -> None:
    valider_email("wissal@example.com")


def test_email_invalide() -> None:
    with pytest.raises(ValidationError):
        valider_email("wissal-example.com")


def test_telephone_valide() -> None:
    valider_telephone("0612345678")


def test_telephone_trop_court() -> None:
    with pytest.raises(ValidationError):
        valider_telephone("061234")


def test_telephone_avec_lettres() -> None:
    with pytest.raises(ValidationError):
        valider_telephone("06AB345678")


def test_mot_de_passe_valide() -> None:
    valider_mot_de_passe("Kampus123")


def test_mot_de_passe_trop_court() -> None:
    with pytest.raises(ValidationError):
        valider_mot_de_passe("Kb123")


def test_mot_de_passe_sans_majuscule() -> None:
    with pytest.raises(ValidationError):
        valider_mot_de_passe("kampus123")


def test_mot_de_passe_sans_chiffre() -> None:
    with pytest.raises(ValidationError):
        valider_mot_de_passe("KampusBank")