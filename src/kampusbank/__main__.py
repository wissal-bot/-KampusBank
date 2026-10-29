"""Point d'entrée de l'application KampusBank."""

from kampusbank.ihm.app import lancer_application


def main() -> None:
    """Démarre KampusBank."""
    lancer_application()


if __name__ == "__main__":
    main()