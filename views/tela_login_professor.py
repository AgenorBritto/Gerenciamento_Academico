
import customtkinter as ctk
from tkinter import messagebox

from views.tela_area_professor import TelaAreaProfessor


class TelaLoginProfessor(ctk.CTkToplevel):

    def __init__(self, master, gerenciamento, gerenciamento_professores):
        super().__init__(master)

        self.gerenciamento = gerenciamento
        self.gerenciamento_professores = gerenciamento_professores

        self.title("Login do Professor")
        self.geometry("480x430")
        self.resizable(False, False)
        self.configure(fg_color="#F8FAFC")

        self.transient(master)
        self.grab_set()

        self.criar_interface()

        self.bind("<Return>", lambda evento: self.entrar())

    def criar_interface(self):

        formulario = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=16,
            border_width=1,
            border_color="#E2E8F0"
        )

        formulario.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=35
        )

        ctk.CTkLabel(
            formulario,
            text="Sistema Acadêmico",
            font=("Arial", 25, "bold"),
            text_color="#6D28D9"
        ).pack(pady=(35, 5))

        ctk.CTkLabel(
            formulario,
            text="Área do Professor",
            font=("Arial", 17, "bold"),
            text_color="#1E293B"
        ).pack(pady=(5, 25))

        ctk.CTkLabel(
            formulario,
            text="Usuário",
            font=("Arial", 13),
            text_color="#334155"
        ).pack(anchor="w", padx=35)

        self.entrada_usuario = ctk.CTkEntry(
            formulario,
            placeholder_text="Digite seu usuário",
            height=40
        )

        self.entrada_usuario.pack(fill="x", padx=35, pady=(5, 15))

        ctk.CTkLabel(
            formulario,
            text="Senha",
            font=("Arial", 13),
            text_color="#334155"
        ).pack(anchor="w", padx=35)

        self.entrada_senha = ctk.CTkEntry(
            formulario,
            placeholder_text="Digite sua senha",
            show="*",
            height=40
        )

        self.entrada_senha.pack(fill="x", padx=35, pady=(5, 20))

        ctk.CTkButton(
            formulario,
            text="Entrar",
            height=42,
            fg_color="#6D28D9",
            hover_color="#5B21B6",
            font=("Arial", 14, "bold"),
            command=self.entrar
        ).pack(fill="x", padx=35, pady=(0, 25))

    def entrar(self):

        usuario = self.entrada_usuario.get()
        senha = self.entrada_senha.get()

        professor = self.gerenciamento_professores.autenticar_professor(
            usuario,
            senha
        )

        if professor is None:
            messagebox.showerror(
                "Falha no login",
                "Usuário ou senha incorretos.",
                parent=self
            )
            self.entrada_senha.delete(0, "end")
            return

        self.destroy()

        TelaAreaProfessor(
            self.master,
            self.gerenciamento,
            professor
        )
