
import customtkinter as ctk
from tkinter import messagebox


class TelaHistoricoAluno(ctk.CTkToplevel):

    def __init__(self, master, gerenciamento, aluno):
        super().__init__(master)

        self.gerenciamento = gerenciamento
        self.aluno = aluno

        self.title("Histórico Acadêmico")
        self.geometry("850x650")
        self.minsize(700, 500)
        self.configure(fg_color="#F8FAFC")

        self.transient(master.winfo_toplevel())

        self.criar_interface()

    def criar_interface(self):

        cabecalho = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=0
        )
        cabecalho.pack(fill="x")

        ctk.CTkLabel(
            cabecalho,
            text="Histórico Acadêmico",
            font=("Arial", 24, "bold"),
            text_color="#6D28D9"
        ).pack(anchor="w", padx=25, pady=(20, 5))

        ctk.CTkLabel(
            cabecalho,
            text=(
                f"Aluno: {self.aluno.get_nome()} | "
                f"Matrícula: {self.aluno.get_matricula()}"
            ),
            font=("Arial", 13),
            text_color="#64748B"
        ).pack(anchor="w", padx=25, pady=(0, 20))

        self.area_historico = ctk.CTkScrollableFrame(
            self,
            fg_color="#F8FAFC",
            corner_radius=0
        )
        self.area_historico.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        self.carregar_historico()

        ctk.CTkButton(
            self,
            text="Fechar",
            width=110,
            height=36,
            fg_color="#6D28D9",
            hover_color="#5B21B6",
            command=self.destroy
        ).pack(pady=(0, 20))

    def carregar_historico(self):

        matriculas = self.gerenciamento.listar_matriculas_aluno(
            self.aluno.get_matricula()
        )

        if not matriculas:
            ctk.CTkLabel(
                self.area_historico,
                text="Este aluno ainda não possui matrículas.",
                font=("Arial", 14),
                text_color="#64748B"
            ).pack(pady=30)

            return

        aprovados = 0
        reprovados = 0
        sem_notas = 0

        for matricula in matriculas:

            situacao = matricula.verificar_situacao()

            if situacao == "Aprovado":
                aprovados += 1
            elif situacao == "Reprovado":
                reprovados += 1
            else:
                sem_notas += 1

        self.criar_resumo(len(matriculas), aprovados, reprovados, sem_notas)

        for matricula in matriculas:
            self.criar_card_disciplina(matricula)

    def criar_resumo(self, total, aprovados, reprovados, sem_notas):

        resumo = ctk.CTkFrame(
            self.area_historico,
            fg_color="transparent"
        )
        resumo.pack(fill="x", pady=(0, 15))

        resumo.grid_columnconfigure((0, 1, 2, 3), weight=1)

        indicadores = [
            ("Disciplinas", total),
            ("Aprovado", aprovados),
            ("Reprovado", reprovados),
            ("Sem notas", sem_notas)
        ]

        for coluna, (titulo, valor) in enumerate(indicadores):

            card = ctk.CTkFrame(
                resumo,
                fg_color="#FFFFFF",
                corner_radius=10,
                border_width=1,
                border_color="#E2E8F0"
            )
            card.grid(
                row=0,
                column=coluna,
                sticky="nsew",
                padx=4
            )

            ctk.CTkLabel(
                card,
                text=titulo,
                font=("Arial", 11),
                text_color="#64748B"
            ).pack(padx=10, pady=(12, 3))

            ctk.CTkLabel(
                card,
                text=str(valor),
                font=("Arial", 22, "bold"),
                text_color="#6D28D9"
            ).pack(padx=10, pady=(0, 12))

    def criar_card_disciplina(self, matricula):

        oferta = matricula.get_oferta()
        disciplina = oferta.get_disciplina()
        professor = oferta.get_professor()

        codigo_aluno = self.aluno.get_matricula()
        codigo_oferta = oferta.get_codigo()

        media = self.gerenciamento.consultar_media(
            codigo_aluno,
            codigo_oferta
        )

        situacao = self.gerenciamento.consultar_situacao(
            codigo_aluno,
            codigo_oferta
        )

        avaliacoes = self.gerenciamento.listar_avaliacoes(
            codigo_aluno,
            codigo_oferta
        )

        card = ctk.CTkFrame(
            self.area_historico,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#E2E8F0"
        )
        card.pack(fill="x", pady=7)

        ctk.CTkLabel(
            card,
            text=disciplina.get_nome(),
            font=("Arial", 17, "bold"),
            text_color="#1E293B"
        ).pack(anchor="w", padx=18, pady=(15, 5))

        informacoes = (
            f"Professor: {professor.get_nome()} | "
            f"Oferta: {oferta.get_codigo()} | "
            f"Seção: {oferta.get_codigo_turma()} | "
            f"Período: {oferta.get_periodo()}"
        )

        ctk.CTkLabel(
            card,
            text=informacoes,
            font=("Arial", 11),
            text_color="#64748B"
        ).pack(anchor="w", padx=18, pady=(0, 12))

        cor = "#64748B"

        if situacao == "Aprovado":
            cor = "#15803D"
        elif situacao == "Reprovado":
            cor = "#DC2626"

        resultado = ctk.CTkFrame(
            card,
            fg_color="#F8FAFC",
            corner_radius=8
        )
        resultado.pack(fill="x", padx=15, pady=(0, 12))

        ctk.CTkLabel(
            resultado,
            text=f"Média: {media:.2f}",
            font=("Arial", 14, "bold"),
            text_color="#6D28D9"
        ).pack(side="left", padx=12, pady=10)

        ctk.CTkLabel(
            resultado,
            text=situacao,
            font=("Arial", 13, "bold"),
            text_color=cor
        ).pack(side="right", padx=12, pady=10)

        ctk.CTkLabel(
            card,
            text="Avaliações",
            font=("Arial", 13, "bold"),
            text_color="#334155"
        ).pack(anchor="w", padx=18, pady=(0, 5))

        if not avaliacoes:

            ctk.CTkLabel(
                card,
                text="Nenhuma avaliação registrada.",
                font=("Arial", 12),
                text_color="#64748B"
            ).pack(anchor="w", padx=18, pady=(0, 15))

        else:

            for avaliacao in avaliacoes:

                texto = (
                    f"{avaliacao['descricao']} — "
                    f"Nota: {avaliacao['nota']:.2f}"
                )

                ctk.CTkLabel(
                    card,
                    text=texto,
                    font=("Arial", 12),
                    text_color="#64748B"
                ).pack(anchor="w", padx=18, pady=(2, 3))

            ctk.CTkLabel(
                card,
                text=f"Total de avaliações: {len(avaliacoes)}",
                font=("Arial", 11),
                text_color="#64748B"
            ).pack(anchor="w", padx=18, pady=(5, 15))
