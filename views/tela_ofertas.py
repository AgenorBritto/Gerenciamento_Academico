import customtkinter as ctk
from tkinter import messagebox

from models.oferta_disciplina import OfertaDisciplina


class TelaOfertas(ctk.CTkFrame):

    def __init__(self, master, gerenciamento):
        super().__init__(master, fg_color="transparent")

        self.gerenciamento = gerenciamento
        self.codigo_selecionado = None

        self.disciplinas_disponiveis = {}
        self.professores_disponiveis = {}

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
            text="Gerenciamento de Ofertas",
            font=("Arial", 26, "bold"),
            text_color="#1E293B"
        )

        titulo.grid(row=0, column=0, sticky="w", pady=(10, 5))

        descricao = ctk.CTkLabel(
            self,
            text="Crie ofertas de disciplinas e defina professores, turmas e vagas.",
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
            text="Dados da oferta",
            font=("Arial", 18, "bold"),
            text_color="#1E293B"
        )

        titulo.grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(20, 15))

        # Código e disciplina
        ctk.CTkLabel(
            formulario,
            text="Código da oferta",
            text_color="#334155"
        ).grid(row=1, column=0, sticky="w", padx=20)

        ctk.CTkLabel(
            formulario,
            text="Disciplina",
            text_color="#334155"
        ).grid(row=1, column=1, sticky="w", padx=20)

        self.entrada_codigo = ctk.CTkEntry(
            formulario,
            placeholder_text="Ex.: BD01",
            height=38
        )

        self.entrada_codigo.grid(row=2, column=0, sticky="ew", padx=20, pady=(5, 15))

        self.selecao_disciplina = ctk.CTkOptionMenu(
            formulario,
            values=["Nenhuma disciplina cadastrada"],
            height=38,
            fg_color="#6D28D9",
            button_color="#5B21B6",
            button_hover_color="#4C1D95"
        )

        self.selecao_disciplina.grid(row=2, column=1, sticky="ew", padx=20, pady=(5, 15))

        # Professor e código da turma
        ctk.CTkLabel(
            formulario,
            text="Professor responsável",
            text_color="#334155"
        ).grid(row=3, column=0, sticky="w", padx=20)

        ctk.CTkLabel(
            formulario,
            text="Seção da oferta",
            text_color="#334155"
        ).grid(row=3, column=1, sticky="w", padx=20)

        self.selecao_professor = ctk.CTkOptionMenu(
            formulario,
            values=["Nenhum professor cadastrado"],
            height=38,
            fg_color="#6D28D9",
            button_color="#5B21B6",
            button_hover_color="#4C1D95"
        )

        self.selecao_professor.grid(row=4, column=0, sticky="ew", padx=20, pady=(5, 15))

        self.entrada_turma = ctk.CTkEntry(
            formulario,
            placeholder_text="Ex.: A",
            height=38
        )

        self.entrada_turma.grid(row=4, column=1, sticky="ew", padx=20, pady=(5, 15))

        # Período e limite de vagas
        ctk.CTkLabel(
            formulario,
            text="Período letivo",
            text_color="#334155"
        ).grid(row=5, column=0, sticky="w", padx=20)

        ctk.CTkLabel(
            formulario,
            text="Limite de vagas",
            text_color="#334155"
        ).grid(row=5, column=1, sticky="w", padx=20)

        self.entrada_periodo = ctk.CTkEntry(
            formulario,
            placeholder_text="Ex.: 2026.1",
            height=38
        )

        self.entrada_periodo.grid(row=6, column=0, sticky="ew", padx=20, pady=(5, 20))

        self.entrada_vagas = ctk.CTkEntry(
            formulario,
            placeholder_text="Ex.: 40",
            height=38
        )

        self.entrada_vagas.insert(0, "40")
        self.entrada_vagas.grid(row=6, column=1, sticky="ew", padx=20, pady=(5, 20))

        # Botões
        botoes = ctk.CTkFrame(formulario, fg_color="transparent")
        botoes.grid(row=7, column=0, columnspan=2, sticky="w", padx=20, pady=(0, 20))

        self.botao_salvar = ctk.CTkButton(
            botoes,
            text="Cadastrar oferta",
            width=150,
            height=38,
            fg_color="#6D28D9",
            hover_color="#5B21B6",
            command=self.salvar_oferta
        )

        self.botao_salvar.pack(side="left", padx=(0, 10))

        ctk.CTkButton(
            botoes,
            text="Limpar",
            width=100,
            height=38,
            fg_color="#E2E8F0",
            hover_color="#CBD5E1",
            text_color="#334155",
            command=self.limpar_formulario
        ).pack(side="left")

    def criar_lista(self):

        titulo = ctk.CTkLabel(
            self,
            text="Ofertas cadastradas",
            font=("Arial", 18, "bold"),
            text_color="#1E293B"
        )

        titulo.grid(row=3, column=0, sticky="w", pady=(0, 10))

        self.lista_ofertas = ctk.CTkScrollableFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#E2E8F0"
        )

        self.lista_ofertas.grid(row=4, column=0, sticky="nsew")

    def atualizar_opcoes(self):

        disciplinas = self.gerenciamento.listar_disciplinas()
        professores = self.gerenciamento.listar_professores()

        self.disciplinas_disponiveis = {}
        self.professores_disponiveis = {}

        for disciplina in disciplinas:
            identificacao = f"{disciplina.get_nome()} ({disciplina.get_codigo()})"
            self.disciplinas_disponiveis[identificacao] = disciplina

        for professor in professores:
            identificacao = f"{professor.get_nome()} ({professor.get_codigo()})"
            self.professores_disponiveis[identificacao] = professor

        opcoes_disciplinas = list(self.disciplinas_disponiveis.keys())
        opcoes_professores = list(self.professores_disponiveis.keys())

        if opcoes_disciplinas:
            self.selecao_disciplina.configure(values=opcoes_disciplinas)
            if self.selecao_disciplina.get() not in opcoes_disciplinas:
                self.selecao_disciplina.set(opcoes_disciplinas[0])
        else:
            self.selecao_disciplina.configure(values=["Nenhuma disciplina cadastrada"])
            self.selecao_disciplina.set("Nenhuma disciplina cadastrada")

        if opcoes_professores:
            self.selecao_professor.configure(values=opcoes_professores)
            if self.selecao_professor.get() not in opcoes_professores:
                self.selecao_professor.set(opcoes_professores[0])
        else:
            self.selecao_professor.configure(values=["Nenhum professor cadastrado"])
            self.selecao_professor.set("Nenhum professor cadastrado")

    def salvar_oferta(self):
        try:
            codigo = self.entrada_codigo.get()
            codigo_turma = self.entrada_turma.get()
            periodo = self.entrada_periodo.get()
            limite_vagas = int(self.entrada_vagas.get())

            disciplina_selecionada = self.selecao_disciplina.get()
            professor_selecionado = self.selecao_professor.get()

            if disciplina_selecionada not in self.disciplinas_disponiveis:
                raise ValueError("Cadastre uma disciplina antes de criar uma oferta.")

            if professor_selecionado not in self.professores_disponiveis:
                raise ValueError("Cadastre um professor antes de criar uma oferta.")

            disciplina = self.disciplinas_disponiveis[disciplina_selecionada]
            professor = self.professores_disponiveis[professor_selecionado]

            if self.codigo_selecionado is None:

                oferta = OfertaDisciplina(
                    codigo,
                    disciplina,
                    professor,
                    codigo_turma,
                    periodo,
                    limite_vagas
                )

                self.gerenciamento.cadastrar_oferta(oferta)

                messagebox.showinfo(
                    "Sucesso",
                    "Oferta cadastrada com sucesso."
                )
                
            else:
                self.gerenciamento.editar_oferta(
                    self.codigo_selecionado,
                    novo_codigo=codigo,
                    nova_disciplina=disciplina,
                    novo_professor=professor,
                    novo_codigo_turma=codigo_turma,
                    novo_periodo=periodo,
                    novo_limite_vagas=limite_vagas
                )

                messagebox.showinfo(
                    "Sucesso",
                    "Dados da oferta atualizados com sucesso."
                )
                

            self.limpar_formulario()
            self.atualizar_lista()

        except (ValueError, TypeError) as erro:
                messagebox.showerror("Erro", str(erro))

    def selecionar_oferta(self, oferta):

        self.limpar_formulario()

        self.entrada_codigo.insert(0, oferta.get_codigo())
        self.entrada_turma.insert(0, oferta.get_codigo_turma())
        self.entrada_periodo.insert(0, oferta.get_periodo())
        self.entrada_vagas.delete(0, "end")
        self.entrada_vagas.insert(0, str(oferta.get_limite_vagas()))

        disciplina = oferta.get_disciplina()
        professor = oferta.get_professor()

        identificacao_disciplina = (
            f"{disciplina.get_nome()} ({disciplina.get_codigo()})"
        )

        identificacao_professor = (
            f"{professor.get_nome()} ({professor.get_codigo()})"
        )

        self.selecao_disciplina.set(identificacao_disciplina)
        self.selecao_professor.set(identificacao_professor)

        self.codigo_selecionado = oferta.get_codigo()

        self.botao_salvar.configure(text="Salvar alterações")

    def excluir_oferta(self, codigo):

        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            "Deseja realmente excluir esta oferta?"
        )

        if confirmar:

            try:
                self.gerenciamento.excluir_oferta(codigo)

                messagebox.showinfo(
                    "Sucesso",
                    "Oferta excluída com sucesso."
                )

                if self.codigo_selecionado == codigo:
                    self.limpar_formulario()

                self.atualizar_lista()

            except (ValueError, TypeError) as erro:
                messagebox.showerror("Erro", str(erro))

    def limpar_formulario(self):

        self.entrada_codigo.delete(0, "end")
        self.entrada_turma.delete(0, "end")
        self.entrada_periodo.delete(0, "end")

        self.entrada_vagas.delete(0, "end")
        self.entrada_vagas.insert(0, "40")

        self.codigo_selecionado = None

        self.atualizar_opcoes()

        self.botao_salvar.configure(text="Cadastrar oferta")

    def atualizar_lista(self):

        for widget in self.lista_ofertas.winfo_children():
            widget.destroy()

        ofertas = self.gerenciamento.listar_ofertas()

        if not ofertas:

            mensagem = ctk.CTkLabel(
                self.lista_ofertas,
                text="Nenhuma oferta cadastrada.",
                font=("Arial", 14),
                text_color="#64748B"
            )

            mensagem.pack(pady=25)
            return

        for oferta in ofertas:

            linha = ctk.CTkFrame(
                self.lista_ofertas,
                fg_color="#F8FAFC",
                corner_radius=8
            )

            linha.pack(fill="x", padx=8, pady=5)

            disciplina = oferta.get_disciplina()
            professor = oferta.get_professor()

            informacoes = (
                f"{disciplina.get_nome()} | "
                f"Oferta: {oferta.get_codigo()} | "
                f"Turma: {oferta.get_codigo_turma()} | "
                f"Professor: {professor.get_nome()} | "
                f"Período: {oferta.get_periodo()} | "
                f"Vagas: {oferta.get_limite_vagas()}"
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
                text="Excluir",
                width=80,
                fg_color="#DC2626",
                hover_color="#B91C1C",
                command=lambda codigo=oferta.get_codigo(): self.excluir_oferta(codigo)
            ).pack(side="right", padx=10, pady=8)

            ctk.CTkButton(
                linha,
                text="Editar",
                width=80,
                fg_color="#6D28D9",
                hover_color="#5B21B6",
                command=lambda item=oferta: self.selecionar_oferta(item)
            ).pack(side="right", padx=5, pady=8)
