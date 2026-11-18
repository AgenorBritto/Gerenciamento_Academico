import customtkinter as ctk

from views.tela_notas import TelaNotas


class TelaAreaProfessor(ctk.CTkToplevel):

    def __init__(self, master, gerenciamento, professor):
        super().__init__(master)

        self.gerenciamento = gerenciamento
        self.professor = professor

        self.title("Área do Professor - Sistema Acadêmico")
        self.state("zoomed")
        self.minsize(900, 600)
        self.configure(fg_color="#F8FAFC")

        self.criar_cabecalho()
        self.criar_area_conteudo()

        self.protocol("WM_DELETE_WINDOW", self.sair)

    def criar_cabecalho(self):

        cabecalho = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=0, height=85)
        cabecalho.pack(fill="x")
        cabecalho.pack_propagate(False)

        ctk.CTkLabel(
            cabecalho,
            text="Área do Professor",
            font=("Arial", 22, "bold"),
            text_color="#6D28D9"
        ).pack(side="left", padx=25)

        ctk.CTkLabel(
            cabecalho,
            text=f"Bem-vindo, {self.professor.get_nome()}",
            font=("Arial", 14),
            text_color="#334155"
        ).pack(side="left", padx=20)

        ctk.CTkButton(
            cabecalho,
            text="Sair",
            width=90,
            height=36,
            fg_color="#DC2626",
            hover_color="#B91C1C",
            command=self.sair
        ).pack(side="right", padx=25)

    def criar_area_conteudo(self):

        self.area_conteudo = ctk.CTkFrame(
            self,
            fg_color="#F8FAFC",
            corner_radius=0
        )

        self.area_conteudo.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=25
        )

        tela_notas = TelaNotas(
            self.area_conteudo,
            self.gerenciamento,
            self.professor
        )

        tela_notas.pack(fill="both", expand=True)

    def sair(self):
        self.destroy()