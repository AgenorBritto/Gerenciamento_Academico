import customtkinter as ctk
from tkinter import messagebox


class TelaNotas(ctk.CTkScrollableFrame):
    def __init__(self, master, gerenciamento, professor):
        super().__init__(master, fg_color="transparent")

        self.gerenciamento = gerenciamento
        self.professor = professor

        self.ofertas_disponiveis = {}
        self.alunos_disponiveis = {}
        self.matricula_selecionada = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)

        self.criar_titulo()
        self.criar_formulario()
        self.criar_resultado()
        self.criar_lista()

        self.atualizar_opcoes_ofertas()

    def criar_titulo(self):

        titulo = ctk.CTkLabel(
            self,
            text="Gerenciamento de Notas",
            font=("Arial", 26, "bold"),
            text_color="#1E293B"
        )

        titulo.grid(row=0, column=0, sticky="w", pady=(10, 5))

        descricao = ctk.CTkLabel(
            self,
            text=f"Bem-vindo, professor {self.professor.get_nome()}. Registre as avaliações dos seus alunos.",
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

        formulario.grid(row=2, column=0, sticky="new", pady=(0, 15))
        formulario.grid_columnconfigure((0, 1), weight=1)

        titulo = ctk.CTkLabel(
            formulario,
            text="Selecionar aluno e registrar avaliação",
            font=("Arial", 18, "bold"),
            text_color="#1E293B"
        )

        titulo.grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(20, 15))

        # Oferta
        ctk.CTkLabel(
            formulario,
            text="Oferta da disciplina",
            text_color="#334155"
        ).grid(row=1, column=0, sticky="w", padx=20)

        self.selecao_oferta = ctk.CTkOptionMenu(
            formulario,
            values=["Nenhuma oferta disponível"],
            height=38,
            fg_color="#6D28D9",
            button_color="#5B21B6",
            button_hover_color="#4C1D95",
            command=self.atualizar_opcoes_alunos
        )

        self.selecao_oferta.grid(
            row=2, column=0, columnspan=2,
            sticky="ew", padx=20, pady=(5, 15)
        )

        # Aluno
        ctk.CTkLabel(
            formulario,
            text="Aluno matriculado",
            text_color="#334155"
        ).grid(row=3, column=0, sticky="w", padx=20)

        self.selecao_aluno = ctk.CTkOptionMenu(
            formulario,
            values=["Nenhum aluno disponível"],
            height=38,
            fg_color="#6D28D9",
            button_color="#5B21B6",
            button_hover_color="#4C1D95",
            command=self.selecionar_aluno
        )

        self.selecao_aluno.grid(
            row=4, column=0, columnspan=2,
            sticky="ew", padx=20, pady=(5, 15)
        )

        # Avaliação
        ctk.CTkLabel(
            formulario,
            text="Descrição da avaliação",
            text_color="#334155"
        ).grid(row=5, column=0, sticky="w", padx=20)

        ctk.CTkLabel(
            formulario,
            text="Nota",
            text_color="#334155"
        ).grid(row=5, column=1, sticky="w", padx=20)

        self.entrada_descricao = ctk.CTkEntry(
            formulario,
            placeholder_text="Ex.: Prova 1",
            height=38
        )

        self.entrada_descricao.grid(
            row=6, column=0, sticky="ew", padx=20, pady=(5, 20)
        )

        self.entrada_nota = ctk.CTkEntry(
            formulario,
            placeholder_text="Ex.: 8.5",
            height=38
        )

        self.entrada_nota.grid(
            row=6, column=1, sticky="ew", padx=20, pady=(5, 20)
        )

        # Botões
        botoes = ctk.CTkFrame(formulario, fg_color="transparent")
        botoes.grid(
            row=7, column=0, columnspan=2,
            sticky="w", padx=20, pady=(0, 20)
        )

        ctk.CTkButton(
            botoes,
            text="Adicionar avaliação",
            width=170,
            height=38,
            fg_color="#6D28D9",
            hover_color="#5B21B6",
            command=self.adicionar_avaliacao
        ).pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            botoes,
            text="Atualizar ofertas",
            width=140,
            height=38,
            fg_color="#E2E8F0",
            hover_color="#CBD5E1",
            text_color="#334155",
            command=self.atualizar_opcoes_ofertas
        ).pack(side="left")

    def criar_resultado(self):

        resultado = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#E2E8F0"
        )

        resultado.grid(row=3, column=0, sticky="ew", pady=(0, 15))
        resultado.grid_columnconfigure((0, 1, 2), weight=1)

        ctk.CTkLabel(
            resultado,
            text="Média",
            font=("Arial", 13),
            text_color="#64748B"
        ).grid(row=0, column=0, pady=(15, 5))

        ctk.CTkLabel(
            resultado,
            text="Situação",
            font=("Arial", 13),
            text_color="#64748B"
        ).grid(row=0, column=1, pady=(15, 5))

        ctk.CTkLabel(
            resultado,
            text="Avaliações",
            font=("Arial", 13),
            text_color="#64748B"
        ).grid(row=0, column=2, pady=(15, 5))

        self.valor_media = ctk.CTkLabel(
            resultado,
            text="--",
            font=("Arial", 22, "bold"),
            text_color="#6D28D9"
        )

        self.valor_media.grid(row=1, column=0, pady=(0, 15))

        self.valor_situacao = ctk.CTkLabel(
            resultado,
            text="--",
            font=("Arial", 16, "bold"),
            text_color="#334155"
        )

        self.valor_situacao.grid(row=1, column=1, pady=(0, 15))

        self.valor_quantidade = ctk.CTkLabel(
            resultado,
            text="0",
            font=("Arial", 22, "bold"),
            text_color="#6D28D9"
        )

        self.valor_quantidade.grid(row=1, column=2, pady=(0, 15))

    def criar_lista(self):

        titulo = ctk.CTkLabel(
            self,
            text="Avaliações registradas",
            font=("Arial", 18, "bold"),
            text_color="#1E293B"
        )

        titulo.grid(row=4, column=0, sticky="w", pady=(0, 10))

        self.lista_avaliacoes = ctk.CTkScrollableFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#E2E8F0"
        )

        self.lista_avaliacoes.grid(row=5, column=0, sticky="nsew")

    def atualizar_opcoes_ofertas(self):

        ofertas = self.gerenciamento.listar_ofertas()

        self.ofertas_disponiveis = {}

        for oferta in ofertas:

            if oferta.get_professor() is not self.professor:
                continue

            disciplina = oferta.get_disciplina()

            identificacao = (
                f"{disciplina.get_nome()} | "
                f"{oferta.get_codigo()} | "
                f"Turma {oferta.get_codigo_turma()}"
            )

            self.ofertas_disponiveis[identificacao] = oferta.get_codigo()

        opcoes = list(self.ofertas_disponiveis.keys())

        if opcoes:

            self.selecao_oferta.configure(values=opcoes)
            self.selecao_oferta.set(opcoes[0])
            self.atualizar_opcoes_alunos(opcoes[0])

        else:

            self.selecao_oferta.configure(values=["Nenhuma oferta disponível"])
            self.selecao_oferta.set("Nenhuma oferta disponível")

            self.alunos_disponiveis = {}
            self.matricula_selecionada = None

            self.selecao_aluno.configure(values=["Nenhum aluno disponível"])
            self.selecao_aluno.set("Nenhum aluno disponível")

            self.atualizar_resultado_vazio()

    def atualizar_opcoes_alunos(self, identificacao):

        if identificacao not in self.ofertas_disponiveis:
            return

        codigo_oferta = self.ofertas_disponiveis[identificacao]

        matriculas = self.gerenciamento.listar_matriculas_oferta(codigo_oferta)

        self.alunos_disponiveis = {}

        for matricula in matriculas:

            aluno = matricula.get_aluno()

            identificacao_aluno = (
                f"{aluno.get_nome()} ({aluno.get_matricula()})"
            )

            self.alunos_disponiveis[identificacao_aluno] = aluno.get_matricula()

        opcoes = list(self.alunos_disponiveis.keys())

        if opcoes:

            self.selecao_aluno.configure(values=opcoes)
            self.selecao_aluno.set(opcoes[0])
            self.selecionar_aluno(opcoes[0])

        else:

            self.selecao_aluno.configure(values=["Nenhum aluno matriculado"])
            self.selecao_aluno.set("Nenhum aluno matriculado")

            self.matricula_selecionada = None
            self.atualizar_resultado_vazio()

    def selecionar_aluno(self, identificacao):

        if identificacao not in self.alunos_disponiveis:
            self.matricula_selecionada = None
            self.atualizar_resultado_vazio()
            return

        matricula_aluno = self.alunos_disponiveis[identificacao]
        identificacao_oferta = self.selecao_oferta.get()

        codigo_oferta = self.ofertas_disponiveis.get(identificacao_oferta)

        if codigo_oferta is None:
            self.matricula_selecionada = None
            self.atualizar_resultado_vazio()
            return

        self.matricula_selecionada = (matricula_aluno, codigo_oferta)

        self.atualizar_lista()

    def adicionar_avaliacao(self):

        try:

            if self.matricula_selecionada is None:
                raise ValueError("Selecione uma oferta e um aluno.")

            descricao = self.entrada_descricao.get()
            nota = float(self.entrada_nota.get().replace(",", "."))

            matricula_aluno, codigo_oferta = self.matricula_selecionada

            self.gerenciamento.adicionar_avaliacao_professor(
                self.professor,
                matricula_aluno,
                codigo_oferta,
                descricao,
                nota
            )

            messagebox.showinfo(
                "Sucesso",
                "Avaliação adicionada com sucesso."
            )

            self.entrada_descricao.delete(0, "end")
            self.entrada_nota.delete(0, "end")

            self.atualizar_lista()

        except (ValueError, TypeError) as erro:
            messagebox.showerror("Erro", str(erro))

    def remover_avaliacao(self, indice):

        confirmar = messagebox.askyesno(
            "Confirmar remoção",
            "Deseja realmente remover esta avaliação?"
        )

        if confirmar:

            try:

                matricula_aluno, codigo_oferta = self.matricula_selecionada

                self.gerenciamento.remover_avaliacao_professor(
                    self.professor,
                    matricula_aluno,
                    codigo_oferta,
                    indice
                )

                messagebox.showinfo(
                    "Sucesso",
                    "Avaliação removida com sucesso."
                )

                self.atualizar_lista()

            except (ValueError, TypeError) as erro:
                messagebox.showerror("Erro", str(erro))

    def atualizar_resultado_vazio(self):

        self.valor_media.configure(text="--")
        self.valor_situacao.configure(text="--")
        self.valor_quantidade.configure(text="0")

        for widget in self.lista_avaliacoes.winfo_children():
            widget.destroy()

        mensagem = ctk.CTkLabel(
            self.lista_avaliacoes,
            text="Selecione uma oferta e um aluno para consultar as avaliações.",
            font=("Arial", 14),
            text_color="#64748B"
        )

        mensagem.pack(pady=25)

    def atualizar_lista(self):

        for widget in self.lista_avaliacoes.winfo_children():
            widget.destroy()

        if self.matricula_selecionada is None:
            self.atualizar_resultado_vazio()
            return

        matricula_aluno, codigo_oferta = self.matricula_selecionada

        avaliacoes = self.gerenciamento.listar_avaliacoes(
            matricula_aluno,
            codigo_oferta
        )

        media = self.gerenciamento.consultar_media(
            matricula_aluno,
            codigo_oferta
        )

        situacao = self.gerenciamento.consultar_situacao(
            matricula_aluno,
            codigo_oferta
        )

        self.valor_media.configure(text=f"{media:.2f}")
        self.valor_situacao.configure(text=situacao)
        self.valor_quantidade.configure(text=str(len(avaliacoes)))

        if not avaliacoes:

            mensagem = ctk.CTkLabel(
                self.lista_avaliacoes,
                text="Nenhuma avaliação registrada para este aluno.",
                font=("Arial", 14),
                text_color="#64748B"
            )

            mensagem.pack(pady=25)
            return

        for indice, avaliacao in enumerate(avaliacoes):

            linha = ctk.CTkFrame(
                self.lista_avaliacoes,
                fg_color="#F8FAFC",
                corner_radius=8
            )

            linha.pack(fill="x", padx=8, pady=5)

            informacoes = (
                f"{avaliacao['descricao']} | "
                f"Nota: {avaliacao['nota']:.2f}"
            )

            ctk.CTkLabel(
                linha,
                text=informacoes,
                font=("Arial", 13),
                text_color="#334155"
            ).pack(side="left", padx=15, pady=15)

            ctk.CTkButton(
                linha,
                text="Remover",
                width=90,
                fg_color="#DC2626",
                hover_color="#B91C1C",
                command=lambda i=indice: self.remover_avaliacao(i)
            ).pack(side="right", padx=10, pady=8)
