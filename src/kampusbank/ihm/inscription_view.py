"""Vue Tkinter du formulaire d'inscription."""

import tkinter as tk
from collections.abc import Callable
from tkinter import ttk


class InscriptionView(ttk.Frame):
    """Formulaire graphique d'inscription."""

    def __init__(
        self,
        parent: tk.Misc,
        on_inscription: Callable[[str, str, str, str, str], None],
        on_retour: Callable[[], None],
    ) -> None:
        super().__init__(parent, padding=30)

        self._on_inscription = on_inscription
        self._on_retour = on_retour

        self._creer_interface()

    def _creer_interface(self) -> None:
        """Crée les champs du formulaire."""

        titre = ttk.Label(
            self,
            text="Créer un compte",
            font=("Arial", 22, "bold"),
        )
        titre.pack(pady=(10, 25))

        self._nom = self._creer_champ("Nom")
        self._prenom = self._creer_champ("Prénom")
        self._email = self._creer_champ("E-mail")
        self._telephone = self._creer_champ("Téléphone")
        self._mot_de_passe = self._creer_champ(
            "Mot de passe",
            masque="*",
        )

        bouton_inscription = ttk.Button(
            self,
            text="S'inscrire",
            command=self._soumettre,
        )
        bouton_inscription.pack(pady=(25, 10))

        bouton_retour = ttk.Button(
            self,
            text="Retour",
            command=self._on_retour,
        )
        bouton_retour.pack()

    def _creer_champ(
        self,
        libelle: str,
        masque: str | None = None,
    ) -> ttk.Entry:
        """Crée un libellé accompagné d'un champ de saisie."""

        label = ttk.Label(self, text=libelle)
        label.pack(anchor="w", pady=(8, 2))

        champ = ttk.Entry(self, width=40)

        if masque is not None:
            champ.configure(show=masque)

        champ.pack(fill="x")

        return champ

    def _soumettre(self) -> None:
        """Transmet les données saisies au contrôleur."""

        self._on_inscription(
            self._nom.get(),
            self._prenom.get(),
            self._email.get(),
            self._telephone.get(),
            self._mot_de_passe.get(),
        )