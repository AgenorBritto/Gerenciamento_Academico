
import customtkinter as ctk
from tkinter import messagebox
from views.tela_historico_aluno import TelaHistoricoAluno
from models.aluno import Aluno


class TelaAlunos(ctk.CTkFrame):

    def __init__(self, master, gerenciamento):
        super().__init__(master, fg_color="transparent")

        self.gerenciamento = gerenciamento
        self.matricula_selecionada = None

        self.grid_columnconfigure(0, weight=1)

        self.criar_titulo()
        self.criar_formulario()
        self.criar_lista()

        self.atualizar_opcoes_turmas()
        self.atualizar_lista()

    def criar_titulo(self):

        titulo = ctk.CTkLabel(
            self,
            text="Gerenciamento de Alunos",
            font=("Arial", 26, "bold"),
            text_color="#1E293B"
        )

        titulo.grid(row=0, column=0, sticky="w", pady=(10, 5))

        descricao = ctk.CTkLabel(
            self,
            text="Cadastre, consulte, edite ou exclua alunos do sistema.",
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
            text="Dados do aluno",
            font=("Arial", 18, "bold"),
            text_color="#1E293B"
        )

        titulo.grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(20, 15))

        # Nome e idade
        ctk.CTkLabel(
            formulario,
            text="Nome",
            text_color="#334155"
        ).grid(row=1, column=0, sticky="w", padx=20)

        ctk.CTkLabel(
            formulario,
            text="Idade",
            text_color="#334155"
        ).grid(row=1, column=1, sticky="w", padx=20)

        self.entrada_nome = ctk.CTkEntry(
            formulario,
            placeholder_text="Nome completo",
            height=38
        )

        self.entrada_nome.grid(row=2, column=0, sticky="ew", padx=20, pady=(5, 15))

        self.entrada_idade = ctk.CTkEntry(
            formulario,
            placeholder_text="Idade",
            height=38
        )

        self.entrada_idade.grid(row=2, column=1, sticky="ew", padx=20, pady=(5, 15))

        # Matrícula e turma
        ctk.CTkLabel(
            formulario,
            text="Matrícula",
            text_color="#334155"
        ).grid(row=3, column=0, sticky="w", padx=20)

        ctk.CTkLabel(
            formulario,
            text="Turma de ingresso",
            text_color="#334155"
        ).grid(row=3, column=1, sticky="w", padx=20)

        self.entrada_matricula = ctk.CTkEntry(
            formulario,
            placeholder_text="Ex.: 2026001",
            height=38
        )

        self.entrada_matricula.grid(row=4, column=0, sticky="ew", padx=20, pady=(5, 20))

        self.entrada_turma = ctk.CTkOptionMenu(
            formulario,
            values=["Selecione uma turma"],
            height=38,
            fg_color="#6D28D9",
            button_color="#5B21B6",
            button_hover_color="#4C1D95",
            dropdown_fg_color="#FFFFFF",
            dropdown_text_color="#334155"
        )

        self.entrada_turma.grid(row=4, column=1, sticky="ew", padx=20, pady=(5, 20))

        # Botões
        botoes = ctk.CTkFrame(formulario, fg_color="transparent")
        botoes.grid(row=5, column=0, columnspan=2, sticky="w", padx=20, pady=(0, 20))

        self.botao_salvar = ctk.CTkButton(
            botoes,
            text="Cadastrar aluno",
            width=150,
            height=38,
            fg_color="#6D28D9",
            hover_color="#5B21B6",
            command=self.salvar_aluno
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
            text="Alunos cadastrados",
            font=("Arial", 18, "bold"),
            text_color="#1E293B"
        )

        titulo.grid(row=3, column=0, sticky="w", pady=(0, 10))

        self.lista_alunos = ctk.CTkScrollableFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#E2E8F0"
        )

        self.lista_alunos.grid(row=4, column=0, sticky="nsew")
        self.grid_rowconfigure(4, weight=1)

    def atualizar_opcoes_turmas(self):

        turmas = self.gerenciamento.listar_turmas()

        opcoes = ["Selecione uma turma"]

        for turma in turmas:
            opcoes.append(turma.get_codigo())

        self.entrada_turma.configure(values=opcoes)

        codigo_atual = self.entrada_turma.get()

        if codigo_atual in opcoes:
            self.entrada_turma.set(codigo_atual)
        else:
            self.entrada_turma.set("Selecione uma turma")

    def salvar_aluno(self):

        try:
            nome = self.entrada_nome.get().strip()
            idade = int(self.entrada_idade.get())
            matricula = self.entrada_matricula.get().strip()

            codigo_turma = self.entrada_turma.get()

            if codigo_turma == "Selecione uma turma":
                raise ValueError("Selecione uma turma para o aluno.")

            turma = self.gerenciamento.buscar_turma(codigo_turma)

            if turma is None:
                raise ValueError("A turma selecionada não foi encontrada.")

            if self.matricula_selecionada is None:

                aluno = Aluno(nome, idade, matricula, turma)

                self.gerenciamento.cadastrar_aluno(aluno)

                messagebox.showinfo(
                    "Sucesso",
                    "Aluno cadastrado com sucesso."
                )

            else:

                self.gerenciamento.editar_aluno(
                    self.matricula_selecionada,
                    novo_nome=nome,
                    nova_idade=idade,
                    nova_matricula=matricula,
                    nova_turma=turma
                )

                messagebox.showinfo(
                    "Sucesso",
                    "Dados do aluno atualizados com sucesso."
                )

            self.limpar_formulario()
            self.atualizar_lista()

        except (ValueError, TypeError) as erro:
            messagebox.showerror("Erro", str(erro))

    def selecionar_aluno(self, aluno):

        self.limpar_formulario()

        self.entrada_nome.insert(0, aluno.get_nome())
        self.entrada_idade.insert(0, str(aluno.get_idade()))
        self.entrada_matricula.insert(0, aluno.get_matricula())
        self.entrada_turma.set(aluno.get_turma().get_codigo())

        self.matricula_selecionada = aluno.get_matricula()

        self.botao_salvar.configure(text="Salvar alterações")

    def excluir_aluno(self, matricula):

        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            "Deseja realmente excluir este aluno?"
        )

        if confirmar:

            try:
                self.gerenciamento.excluir_aluno(matricula)

                messagebox.showinfo(
                    "Sucesso",
                    "Aluno excluído com sucesso."
                )

                if self.matricula_selecionada == matricula:
                    self.limpar_formulario()

                self.atualizar_lista()

            except (ValueError, TypeError) as erro:
                messagebox.showerror("Erro", str(erro))

    def limpar_formulario(self):

        self.entrada_nome.delete(0, "end")
        self.entrada_idade.delete(0, "end")
        self.entrada_matricula.delete(0, "end")

        self.matricula_selecionada = None

        self.atualizar_opcoes_turmas()

        self.botao_salvar.configure(text="Cadastrar aluno")

    def atualizar_lista(self):

        for widget in self.lista_alunos.winfo_children():
            widget.destroy()

        alunos = self.gerenciamento.listar_alunos()

        if not alunos:

            mensagem = ctk.CTkLabel(
                self.lista_alunos,
                text="Nenhum aluno cadastrado.",
                font=("Arial", 14),
                text_color="#64748B"
            )

            mensagem.pack(pady=25)
            return

        for aluno in alunos:

            linha = ctk.CTkFrame(
                self.lista_alunos,
                fg_color="#F8FAFC",
                corner_radius=8
            )

            linha.pack(fill="x", padx=8, pady=5)

            informacoes = (
                f"{aluno.get_nome()} | "
                f"Matrícula: {aluno.get_matricula()} | "
                f"Turma: {aluno.get_turma().get_codigo()}"
            )

            ctk.CTkLabel(
                linha,
                text=informacoes,
                font=("Arial", 13),
                text_color="#334155"
            ).pack(side="left", padx=15, pady=15)

            ctk.CTkButton(
                linha,
                text="Excluir",
                width=80,
                fg_color="#DC2626",
                hover_color="#B91C1C",
                command=lambda matricula=aluno.get_matricula(): self.excluir_aluno(matricula)
            ).pack(side="right", padx=10, pady=8)

            ctk.CTkButton(
                linha,
                text="Editar",
                width=80,
                fg_color="#6D28D9",
                hover_color="#5B21B6",
                command=lambda estudante=aluno: self.selecionar_aluno(estudante)
            ).pack(side="right", padx=5, pady=8)

            ctk.CTkButton(
                linha,
                text="Histórico",
                width=90,
                fg_color="#0F766E",
                hover_color="#115E59",
                command=lambda estudante=aluno: self.abrir_historico(estudante)
            ).pack(side="right", padx=5, pady=8)
    
    def abrir_historico(self, aluno):
        TelaHistoricoAluno(self, self.gerenciamento, aluno)