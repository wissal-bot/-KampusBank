"""Modèle métier représentant un utilisateur de KampusBank."""

from dataclasses import dataclass
from enum import Enum


class Role(str, Enum):
    """Rôles disponibles dans l'application."""

    CLIENT = "client"
    ADMIN = "admin"


@dataclass
class User:
    """Représente un utilisateur de KampusBank."""

    id: str
    nom: str
    prenom: str
    email: str
    telephone: str
    mot_de_passe_hash: str
    role: Role = Role.CLIENT
    est_bloque: bool = False
    tentatives_connexion: int = 0