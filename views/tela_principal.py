import customtkinter as ctk

from views.tela_alunos import TelaAlunos
from views.tela_professores import TelaProfessores
from views.tela_disciplinas import TelaDisciplinas
from views.tela_matriculas import TelaMatriculas
from views.tela_situacao import TelaSituacao
from views.tela_turmas import TelaTurmas
from views.tela_ofertas import TelaOfertas
from views.tela_login_professor import TelaLoginProfessor


class TelaPrincipal(ctk.CTk):

    def __init__(self, gerenciamento, gerenciamento_professores):
        super().__init__()

        self.gerenciamento = gerenciamento
        self.gerenciamento_professores = gerenciamento_professores
        self.janela_login = None

        # Configurações da janela
        self.title("Sistema de Gerenciamento Acadêmico")
        self.geometry("1100x700")
        self.minsize(900, 600)
        self.configure(fg_color="#F8FAFC")

        # Configuração do layout principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.criar_menu_lateral()
        self.criar_area_conteudo()

        self.mostrar_pagina("Dashboard")

    def criar_menu_lateral(self):

        self.menu_lateral = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0,
            fg_color="#FFFFFF"
        )

        self.menu_lateral.grid(row=0, column=0, sticky="nsew")
        self.menu_lateral.grid_propagate(False)

        # Nome do sistema
        self.logo = ctk.CTkLabel(
            self.menu_lateral,
            text="Sistema\nAcadêmico",
            font=("Arial", 22, "bold"),
            text_color="#6D28D9"
        )

        self.logo.pack(pady=(35, 35))

        # Opções do menu administrativo
        ctk.CTkLabel(
            self.menu_lateral,
            text="ADMINISTRAÇÃO",
            font=("Arial", 11, "bold"),
            text_color="#94A3B8"
        ).pack(anchor="w", padx=20, pady=(0, 10))

        opcoes = [
            "Dashboard",
            "Alunos",
            "Professores",
            "Disciplinas",
            "Turmas",
            "Ofertas",
            "Matrículas",
            "Situação acadêmica"
        ]

        for opcao in opcoes:

            botao = ctk.CTkButton(
                self.menu_lateral,
                text=opcao,
                height=42,
                anchor="w",
                corner_radius=8,
                fg_color="transparent",
                hover_color="#F3E8FF",
                text_color="#334155",
                font=("Arial", 14),
                command=lambda pagina=opcao: self.mostrar_pagina(pagina)
            )

            botao.pack(fill="x", padx=15, pady=3)

        # Separação da área do professor
        ctk.CTkFrame(
            self.menu_lateral,
            height=2,
            fg_color="#E2E8F0"
        ).pack(fill="x", padx=15, pady=20)

        ctk.CTkLabel(
            self.menu_lateral,
            text="ACESSO",
            font=("Arial", 11, "bold"),
            text_color="#94A3B8"
        ).pack(anchor="w", padx=20, pady=(0, 10))

        botao_professor = ctk.CTkButton(
            self.menu_lateral,
            text="Área do Professor",
            height=42,
            anchor="w",
            corner_radius=8,
            fg_color="#6D28D9",
            hover_color="#5B21B6",
            text_color="#FFFFFF",
            font=("Arial", 14, "bold"),
            command=self.abrir_login_professor        )

        botao_professor.pack(fill="x", padx=15, pady=3)

    def criar_area_conteudo(self):

        self.area_conteudo = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color="#F8FAFC"
        )

        self.area_conteudo.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=30,
            pady=25
        )

        self.area_conteudo.grid_columnconfigure(0, weight=1)

    def mostrar_pagina(self, pagina):

        # Limpa a página anterior
        for widget in self.area_conteudo.winfo_children():
            widget.destroy()

        # Telas já implementadas
        telas = {
            "Alunos": TelaAlunos,
            "Disciplinas": TelaDisciplinas,
            "Matrículas": TelaMatriculas,
            "Situação acadêmica": TelaSituacao,
            "Turmas": TelaTurmas,
            "Ofertas": TelaOfertas,
        }
        if pagina == "Professores":
            tela = TelaProfessores(
                self.area_conteudo,
                self.gerenciamento,
                self.gerenciamento_professores
            )
            tela.pack(fill="both", expand=True)
            return

        if pagina in telas:

            tela = telas[pagina](self.area_conteudo, self.gerenciamento)
            tela.pack(fill="both", expand=True)
            return

        # Telas que serão implementadas
        if pagina in ["Área do Professor"]:

            titulo = ctk.CTkLabel(
                self.area_conteudo,
                text=pagina,
                font=("Arial", 28, "bold"),
                text_color="#1E293B"
            )

            titulo.pack(anchor="w", pady=(10, 5))

            mensagem = ctk.CTkLabel(
                self.area_conteudo,
                text=f"A tela de {pagina} será implementada nesta etapa.",
                font=("Arial", 15),
                text_color="#64748B"
            )

            mensagem.pack(anchor="w", pady=20)
            return

        # Dashboard
        if pagina == "Dashboard":

            titulo = ctk.CTkLabel(
                self.area_conteudo,
                text="Dashboard",
                font=("Arial", 28, "bold"),
                text_color="#1E293B"
            )

            titulo.pack(anchor="w", pady=(10, 5))

            self.mostrar_dashboard()

    def mostrar_dashboard(self):

        descricao = ctk.CTkLabel(
            self.area_conteudo,
            text="Bem-vindo ao Sistema de Gerenciamento Acadêmico.",
            font=("Arial", 15),
            text_color="#64748B"
        )

        descricao.pack(anchor="w", pady=(5, 25))

        # Indicadores do sistema
        indicadores = [
            ("Alunos cadastrados", len(self.gerenciamento.listar_alunos())),
            ("Professores cadastrados", len(self.gerenciamento.listar_professores())),
            ("Disciplinas cadastradas", len(self.gerenciamento.listar_disciplinas())),
            ("Turmas cadastradas", len(self.gerenciamento.listar_turmas())),
            ("Ofertas cadastradas", len(self.gerenciamento.listar_ofertas())),
            ("Matrículas realizadas", len(self.gerenciamento.listar_matriculas()))
        ]

        grade = ctk.CTkFrame(
            self.area_conteudo,
            fg_color="transparent"
        )

        grade.pack(fill="x", pady=10)
        grade.grid_columnconfigure((0, 1), weight=1)

        for indice, (nome, quantidade) in enumerate(indicadores):

            linha = indice // 2
            coluna = indice % 2

            card = ctk.CTkFrame(
                grade,
                fg_color="#FFFFFF",
                corner_radius=12,
                border_width=1,
                border_color="#E2E8F0"
            )

            card.grid(
                row=linha,
                column=coluna,
                sticky="nsew",
                padx=8,
                pady=8
            )

            ctk.CTkLabel(
                card,
                text=nome,
                font=("Arial", 14),
                text_color="#64748B"
            ).pack(anchor="w", padx=20, pady=(20, 5))

            ctk.CTkLabel(
                card,
                text=str(quantidade),
                font=("Arial", 30, "bold"),
                text_color="#6D28D9"
            ).pack(anchor="w", padx=20, pady=(0, 20))

        self.mostrar_pessoas_cadastradas()

    def mostrar_pessoas_cadastradas(self):

        ctk.CTkLabel(
            self.area_conteudo,
            text="Pessoas cadastradas",
            font=("Arial", 18, "bold"),
            text_color="#1E293B"
        ).pack(anchor="w", pady=(20, 8))

        lista = ctk.CTkScrollableFrame(
            self.area_conteudo,
            height=160,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#E2E8F0"
        )

        lista.pack(fill="x", pady=(0, 10))

        pessoas = self.gerenciamento.listar_pessoas()

        if not pessoas:
            ctk.CTkLabel(
                lista,
                text="Nenhum aluno ou professor cadastrado ainda.",
                font=("Arial", 14),
                text_color="#94A3B8"
            ).pack(anchor="w", padx=15, pady=10)
            return

        # Polimorfismo: a mesma chamada apresentar() produz um texto
        # diferente para Aluno e para Professor, sem nenhum if por tipo.
        for pessoa in pessoas:
            ctk.CTkLabel(
                lista,
                text=pessoa.apresentar(),
                font=("Arial", 14),
                text_color="#334155",
                anchor="w"
            ).pack(fill="x", padx=15, pady=4)

    def abrir_login_professor(self):

        if self.janela_login is not None and self.janela_login.winfo_exists():
            self.janela_login.focus()
            return

        self.janela_login = TelaLoginProfessor(
            self,
            self.gerenciamento,
            self.gerenciamento_professores
        )