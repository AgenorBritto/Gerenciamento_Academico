
import customtkinter as ctk
from tkinter import messagebox


class TelaMatriculas(ctk.CTkFrame):

    def __init__(self, master, gerenciamento):
        super().__init__(master, fg_color="transparent")

        self.gerenciamento = gerenciamento
        self.alunos_disponiveis = {}
        self.ofertas_disponiveis = {}

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.criar_titulo()
        self.criar_formulario()
        self.criar_lista()

        self.atualizar_opcoes()
        self.atualizar_lista()

    def criar_titulo(self):

        titulo = ctk.CTkLabel(
            self,
            text="Gerenciamento de Matrículas",
            font=("Arial", 26, "bold"),
            text_color="#1E293B"
        )

        titulo.grid(row=0, column=0, sticky="w", pady=(10, 5))

        descricao = ctk.CTkLabel(
            self,
            text="Matricule alunos nas ofertas de disciplinas disponíveis.",
            font=("Arial", 14),
            text_color="#64748B"
        )

        descricao.grid(row=1, column=0, sticky="w", pady=(0, 20))

    def criar_formulario(self):

        formulario = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#E2E8F0"
        )

        formulario.grid(row=2, column=0, sticky="new", pady=(0, 20))
        formulario.grid_columnconfigure((0, 1), weight=1)

        titulo = ctk.CTkLabel(
            formulario,
            text="Nova matrícula",
            font=("Arial", 18, "bold"),
            text_color="#1E293B"
        )

        titulo.grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(20, 15))

        # Seleção do aluno
        ctk.CTkLabel(
            formulario,
            text="Aluno",
            text_color="#334155"
        ).grid(row=1, column=0, sticky="w", padx=20)

        self.selecao_aluno = ctk.CTkOptionMenu(
            formulario,
            values=["Nenhum aluno cadastrado"],
            height=38,
            fg_color="#6D28D9",
            button_color="#5B21B6",
            button_hover_color="#4C1D95"
        )

        self.selecao_aluno.grid(row=2, column=0, sticky="ew", padx=20, pady=(5, 15))

        # Seleção da oferta
        ctk.CTkLabel(
            formulario,
            text="Oferta da disciplina",
            text_color="#334155"
        ).grid(row=1, column=1, sticky="w", padx=20)

        self.selecao_oferta = ctk.CTkOptionMenu(
            formulario,
            values=["Nenhuma oferta cadastrada"],
            height=38,
            fg_color="#6D28D9",
            button_color="#5B21B6",
            button_hover_color="#4C1D95"
        )

        self.selecao_oferta.grid(row=2, column=1, sticky="ew", padx=20, pady=(5, 15))

        # Botões
        botoes = ctk.CTkFrame(formulario, fg_color="transparent")
        botoes.grid(row=3, column=0, columnspan=2, sticky="w", padx=20, pady=(0, 20))

        ctk.CTkButton(
            botoes,
            text="Realizar matrícula",
            width=170,
            height=38,
            fg_color="#6D28D9",
            hover_color="#5B21B6",
            command=self.realizar_matricula
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            botoes,
            text="Atualizar opções",
            width=130,
            height=38,
            fg_color="#64748B",
            hover_color="#475569",
            command=self.atualizar_opcoes
        ).pack(side="left")

    def criar_lista(self):

        titulo = ctk.CTkLabel(
            self,
            text="Matrículas realizadas",
            font=("Arial", 18, "bold"),
            text_color="#1E293B"
        )

        titulo.grid(row=3, column=0, sticky="w", pady=(0, 10))

        self.lista_matriculas = ctk.CTkScrollableFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#E2E8F0"
        )

        self.lista_matriculas.grid(row=4, column=0, sticky="nsew")

    def atualizar_opcoes(self):

        alunos = self.gerenciamento.listar_alunos()
        ofertas = self.gerenciamento.listar_ofertas()

        self.alunos_disponiveis = {}
        self.ofertas_disponiveis = {}

        for aluno in alunos:
            identificacao = f"{aluno.get_nome()} ({aluno.get_matricula()})"
            self.alunos_disponiveis[identificacao] = aluno.get_matricula()

        for oferta in ofertas:

            disciplina = oferta.get_disciplina()
            professor = oferta.get_professor()

            identificacao = (
                f"{disciplina.get_nome()} | "
                f"{oferta.get_codigo()} | "
                f"Turma {oferta.get_codigo_turma()} | "
                f"{professor.get_nome()}"
            )

            self.ofertas_disponiveis[identificacao] = oferta.get_codigo()

        # Atualiza opções de alunos
        opcoes_alunos = list(self.alunos_disponiveis.keys())

        if opcoes_alunos:
            self.selecao_aluno.configure(values=opcoes_alunos)

            if self.selecao_aluno.get() not in opcoes_alunos:
                self.selecao_aluno.set(opcoes_alunos[0])
        else:
            self.selecao_aluno.configure(values=["Nenhum aluno cadastrado"])
            self.selecao_aluno.set("Nenhum aluno cadastrado")

        # Atualiza opções de ofertas
        opcoes_ofertas = list(self.ofertas_disponiveis.keys())

        if opcoes_ofertas:
            self.selecao_oferta.configure(values=opcoes_ofertas)

            if self.selecao_oferta.get() not in opcoes_ofertas:
                self.selecao_oferta.set(opcoes_ofertas[0])
        else:
            self.selecao_oferta.configure(values=["Nenhuma oferta cadastrada"])
            self.selecao_oferta.set("Nenhuma oferta cadastrada")

    def realizar_matricula(self):

        try:
            aluno_selecionado = self.selecao_aluno.get()
            oferta_selecionada = self.selecao_oferta.get()

            if aluno_selecionado not in self.alunos_disponiveis:
                raise ValueError("Cadastre um aluno antes de realizar uma matrícula.")

            if oferta_selecionada not in self.ofertas_disponiveis:
                raise ValueError("Cadastre uma oferta antes de realizar uma matrícula.")

            matricula_aluno = self.alunos_disponiveis[aluno_selecionado]
            codigo_oferta = self.ofertas_disponiveis[oferta_selecionada]

            self.gerenciamento.matricular_aluno(
                matricula_aluno,
                codigo_oferta
            )

            messagebox.showinfo(
                "Sucesso",
                "Matrícula realizada com sucesso."
            )

            self.atualizar_lista()

        except (ValueError, TypeError) as erro:
            messagebox.showerror("Erro", str(erro))

    def remover_matricula(self, matricula_aluno, codigo_oferta):

        confirmar = messagebox.askyesno(
            "Confirmar remoção",
            "Deseja realmente remover esta matrícula?"
        )

        if confirmar:

            try:
                self.gerenciamento.remover_matricula(
                    matricula_aluno,
                    codigo_oferta
                )

                messagebox.showinfo(
                    "Sucesso",
                    "Matrícula removida com sucesso."
                )

                self.atualizar_lista()

            except (ValueError, TypeError) as erro:
                messagebox.showerror("Erro", str(erro))

    def atualizar_lista(self):

        for widget in self.lista_matriculas.winfo_children():
            widget.destroy()

        matriculas = self.gerenciamento.listar_matriculas()

        if not matriculas:

            mensagem = ctk.CTkLabel(
                self.lista_matriculas,
                text="Nenhuma matrícula realizada.",
                font=("Arial", 14),
                text_color="#64748B"
            )

            mensagem.pack(pady=25)
            return

        for matricula in matriculas:

            aluno = matricula.get_aluno()
            oferta = matricula.get_oferta()

            disciplina = oferta.get_disciplina()
            professor = oferta.get_professor()

            linha = ctk.CTkFrame(
                self.lista_matriculas,
                fg_color="#F8FAFC",
                corner_radius=8
            )

            linha.pack(fill="x", padx=8, pady=5)

            informacoes = (
                f"{aluno.get_nome()} | {aluno.get_matricula()}  →  "
                f"{disciplina.get_nome()} | Oferta: {oferta.get_codigo()} | "
                f"Turma: {oferta.get_codigo_turma()} | "
                f"Professor: {professor.get_nome()}"
            )

            ctk.CTkLabel(
                linha,
                text=informacoes,
                font=("Arial", 13),
                text_color="#334155",
                anchor="w",
                justify="left"
            ).pack(side="left", fill="x", expand=True, padx=15, pady=15)

            ctk.CTkButton(
                linha,
                text="Remover",
                width=90,
                fg_color="#DC2626",
                hover_color="#B91C1C",
                command=lambda m=aluno.get_matricula(), o=oferta.get_codigo(): self.remover_matricula(m, o)
            ).pack(side="right", padx=10, pady=8)
