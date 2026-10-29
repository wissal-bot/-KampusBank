"""Fonctions de validation des données métier de KampusBank."""

import re

from kampusbank.domaine.exceptions import ValidationError


def valider_email(email: str) -> None:
    """Vérifie que l'adresse e-mail possède un format valide."""
    motif = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"

    if not re.fullmatch(motif, email):
        raise ValidationError("L'adresse e-mail est invalide.")


def valider_telephone(telephone: str) -> None:
    """Vérifie que le téléphone contient exactement 10 chiffres."""
    if len(telephone) != 10 or not telephone.isdigit():
        raise ValidationError(
            "Le numéro de téléphone doit contenir exactement 10 chiffres."
        )


def valider_mot_de_passe(mot_de_passe: str) -> None:
    """Vérifie que le mot de passe respecte les règles de sécurité."""
    if len(mot_de_passe) < 8:
        raise ValidationError(
            "Le mot de passe doit contenir au moins 8 caractères."
        )

    if not any(caractere.isupper() for caractere in mot_de_passe):
        raise ValidationError(
            "Le mot de passe doit contenir au moins une majuscule."
        )

    if not any(caractere.isdigit() for caractere in mot_de_passe):
        raise ValidationError(
            "Le mot de passe doit contenir au moins un chiffre."
        )