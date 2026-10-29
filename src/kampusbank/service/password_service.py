"""Service de gestion sécurisée des mots de passe."""

import bcrypt


def hacher_mot_de_passe(mot_de_passe: str) -> str:
    """Hache un mot de passe avec bcrypt."""
    mot_de_passe_bytes = mot_de_passe.encode("utf-8")

    hash_bytes = bcrypt.hashpw(
        mot_de_passe_bytes,
        bcrypt.gensalt(),
    )

    return hash_bytes.decode("utf-8")


def verifier_mot_de_passe(
    mot_de_passe: str,
    mot_de_passe_hash: str,
) -> bool:
    """Vérifie qu'un mot de passe correspond à un hash bcrypt."""
    return bcrypt.checkpw(
        mot_de_passe.encode("utf-8"),
        mot_de_passe_hash.encode("utf-8"),
    )