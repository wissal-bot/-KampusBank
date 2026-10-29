"""Fenêtre principale de l'application KampusBank."""

import tkinter as tk
from tkinter import messagebox, ttk

from kampusbank.domaine.exceptions import KampusBankError
from kampusbank.ihm.connexion_view import ConnexionView
from kampusbank.ihm.inscription_view import InscriptionView
from kampusbank.persistance.user_repository import InMemoryUserRepository
from kampusbank.service.authentification_service import (
    AuthentificationService,
)
from kampusbank.service.inscription_service import InscriptionService
from kampusbank.service.session_service import SessionService


class KampusBankApp(tk.Tk):
    """Fenêtre principale de KampusBank."""

    def __init__(self) -> None:
        super().__init__()

        self.title("KampusBank")
        self.geometry("500x550")
        self.resizable(False, False)

        # Dépôt temporaire des utilisateurs en mémoire.
        self._repository = InMemoryUserRepository()

        # Services métier.
        self._inscription_service = InscriptionService(
            self._repository
        )

        self._authentification_service = AuthentificationService(
            self._repository
        )

        self._session_service = SessionService()

        # Affichage initial.
        self._afficher_accueil()

    def _effacer_fenetre(self) -> None:
        """Supprime les composants actuellement affichés."""
        for composant in self.winfo_children():
            composant.destroy()

    def _afficher_accueil(self) -> None:
        """Affiche l'écran d'accueil."""
        self._effacer_fenetre()

        conteneur = ttk.Frame(
            self,
            padding=40,
        )
        conteneur.pack(
            expand=True,
            fill="both",
        )

        titre = ttk.Label(
            conteneur,
            text="KampusBank",
            font=("Arial", 26, "bold"),
        )
        titre.pack(
            pady=(80, 10),
        )

        sous_titre = ttk.Label(
            conteneur,
            text="Votre banque universitaire",
            font=("Arial", 12),
        )
        sous_titre.pack(
            pady=(0, 40),
        )

        bouton_connexion = ttk.Button(
            conteneur,
            text="Se connecter",
            command=self._afficher_connexion,
        )
        bouton_connexion.pack(
            pady=10,
            ipadx=30,
            ipady=8,
        )

        bouton_inscription = ttk.Button(
            conteneur,
            text="S'inscrire",
            command=self._afficher_inscription,
        )
        bouton_inscription.pack(
            pady=10,
            ipadx=40,
            ipady=8,
        )

    def _afficher_inscription(self) -> None:
        """Affiche le formulaire d'inscription."""
        self._effacer_fenetre()

        vue = InscriptionView(
            self,
            on_inscription=self._inscrire,
            on_retour=self._afficher_accueil,
        )

        vue.pack(
            expand=True,
            fill="both",
        )

    def _inscrire(
        self,
        nom: str,
        prenom: str,
        email: str,
        telephone: str,
        mot_de_passe: str,
    ) -> None:
        """Traite une demande d'inscription."""

        try:
            self._inscription_service.inscrire(
                nom=nom,
                prenom=prenom,
                email=email,
                telephone=telephone,
                mot_de_passe=mot_de_passe,
            )

        except KampusBankError as erreur:
            messagebox.showerror(
                "Erreur",
                str(erreur),
            )
            return

        messagebox.showinfo(
            "Inscription réussie",
            "Votre compte KampusBank a été créé.",
        )

        self._afficher_accueil()

    def _afficher_connexion(self) -> None:
        """Affiche le formulaire de connexion."""
        self._effacer_fenetre()

        vue = ConnexionView(
            self,
            on_connexion=self._connecter,
            on_retour=self._afficher_accueil,
        )

        vue.pack(
            expand=True,
            fill="both",
        )

    def _connecter(
        self,
        email: str,
        mot_de_passe: str,
    ) -> None:
        """Traite une demande de connexion."""

        try:
            user = self._authentification_service.connecter(
                email,
                mot_de_passe,
            )

        except KampusBankError as erreur:
            messagebox.showerror(
                "Connexion impossible",
                str(erreur),
            )
            return

        self._session_service.ouvrir_session(user)

        messagebox.showinfo(
            "Connexion réussie",
            f"Bienvenue {user.prenom} {user.nom}.",
        )

        self._afficher_espace_client()

    def _afficher_espace_client(self) -> None:
        """Affiche l'espace du client connecté."""
        self._effacer_fenetre()

        user = self._session_service.exiger_utilisateur_connecte()

        conteneur = ttk.Frame(
            self,
            padding=40,
        )
        conteneur.pack(
            expand=True,
            fill="both",
        )

        titre = ttk.Label(
            conteneur,
            text=f"Bienvenue {user.prenom}",
            font=("Arial", 22, "bold"),
        )
        titre.pack(
            pady=(60, 15),
        )

        email = ttk.Label(
            conteneur,
            text=user.email,
        )
        email.pack(
            pady=5,
        )

        bouton_deconnexion = ttk.Button(
            conteneur,
            text="Se déconnecter",
            command=self._deconnecter,
        )
        bouton_deconnexion.pack(
            pady=30,
        )

    def _deconnecter(self) -> None:
        """Déconnecte l'utilisateur."""
        self._session_service.fermer_session()
        self._afficher_accueil()


def lancer_application() -> None:
    """Lance l'application KampusBank."""
    application = KampusBankApp()
    application.mainloop()