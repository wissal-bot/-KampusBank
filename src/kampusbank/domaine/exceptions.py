"""Exceptions métier de l'application KampusBank."""


class KampusBankError(Exception):
    """Exception de base de l'application KampusBank."""


class ValidationError(KampusBankError):
    """Erreur déclenchée lorsqu'une donnée saisie est invalide."""


class EmailDejaUtiliseError(KampusBankError):
    """Erreur déclenchée lorsqu'une adresse e-mail existe déjà."""


class AuthentificationError(KampusBankError):
    """Erreur déclenchée lorsque l'authentification échoue."""


class UtilisateurBloqueError(KampusBankError):
    """Erreur déclenchée lorsqu'un utilisateur est temporairement bloqué."""