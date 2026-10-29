"""Vue Tkinter du formulaire de connexion."""

import tkinter as tk
from collections.abc import Callable
from tkinter import ttk


class ConnexionView(ttk.Frame):
    """Formulaire graphique de connexion."""

    def __init__(
        self,
        parent: tk.Misc,
        on_connexion: Callable[[str, str], None],
        on_retour: Callable[[], None],
    ) -> None:
        super().__init__(parent, padding=30)

        self._on_connexion = on_connexion
        self._on_retour = on_retour

        self._creer_interface()

    def _creer_interface(self) -> None:
        """Crée le formulaire de connexion."""

        titre = ttk.Label(
            self,
            text="Se connecter",
            font=("Arial", 22, "bold"),
        )
        titre.pack(pady=(60, 30))

        label_email = ttk.Label(self, text="E-mail")
        label_email.pack(anchor="w", pady=(8, 2))

        self._email = ttk.Entry(self, width=40)
        self._email.pack(fill="x")

        label_mot_de_passe = ttk.Label(
            self,
            text="Mot de passe",
        )
        label_mot_de_passe.pack(anchor="w", pady=(15, 2))

        self._mot_de_passe = ttk.Entry(
            self,
            width=40,
            show="*",
        )
        self._mot_de_passe.pack(fill="x")

        bouton_connexion = ttk.Button(
            self,
            text="Se connecter",
            command=self._soumettre,
        )
        bouton_connexion.pack(pady=(30, 10))

        bouton_retour = ttk.Button(
            self,
            text="Retour",
            command=self._on_retour,
        )
        bouton_retour.pack()

    def _soumettre(self) -> None:
        """Transmet les identifiants saisis."""

        self._on_connexion(
            self._email.get(),
            self._mot_de_passe.get(),
        )