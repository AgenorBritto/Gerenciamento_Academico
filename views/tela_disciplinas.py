
import customtkinter as ctk
from tkinter import messagebox
from models.disciplina import Disciplina


class TelaDisciplinas(ctk.CTkFrame):

    def __init__(self, master, gerenciamento):
        super().__init__(master, fg_color="transparent")

        self.gerenciamento = gerenciamento
        self.codigo_selecionado = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.criar_titulo()
        self.criar_formulario()
        self.criar_lista()

        self.atualizar_lista()

    def criar_titulo(self):

        titulo = ctk.CTkLabel(
            self,
            text="Gerenciamento de Disciplinas",
            font=("Arial", 26, "bold"),
            text_color="#1E293B"
        )

        titulo.grid(row=0, column=0, sticky="w", pady=(10, 5))

        descricao = ctk.CTkLabel(
            self,
            text="Cadastre, consulte, edite ou exclua disciplinas do sistema.",
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
            text="Dados da disciplina",
            font=("Arial", 18, "bold"),
            text_color="#1E293B"
        )

        titulo.grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(20, 15))

        # Código
        ctk.CTkLabel(
            formulario,
            text="Código",
            text_color="#334155"
        ).grid(row=1, column=0, sticky="w", padx=20)

        self.entrada_codigo = ctk.CTkEntry(
            formulario,
            placeholder_text="Ex.: D001",
            height=38
        )

        self.entrada_codigo.grid(row=2, column=0, sticky="ew", padx=20, pady=(5, 20))

        # Nome
        ctk.CTkLabel(
            formulario,
            text="Nome",
            text_color="#334155"
        ).grid(row=1, column=1, sticky="w", padx=20)

        self.entrada_nome = ctk.CTkEntry(
            formulario,
            placeholder_text="Nome da disciplina",
            height=38
        )

        self.entrada_nome.grid(row=2, column=1, sticky="ew", padx=20, pady=(5, 20))

        # Botões
        botoes = ctk.CTkFrame(formulario, fg_color="transparent")
        botoes.grid(row=3, column=0, columnspan=2, sticky="w", padx=20, pady=(0, 20))

        self.botao_salvar = ctk.CTkButton(
            botoes,
            text="Cadastrar disciplina",
            width=170,
            height=38,
            fg_color="#6D28D9",
            hover_color="#5B21B6",
            command=self.salvar_disciplina
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
            text="Disciplinas cadastradas",
            font=("Arial", 18, "bold"),
            text_color="#1E293B"
        )

        titulo.grid(row=3, column=0, sticky="w", pady=(0, 10))

        self.lista_disciplinas = ctk.CTkScrollableFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#E2E8F0"
        )

        self.lista_disciplinas.grid(row=4, column=0, sticky="nsew")

    def salvar_disciplina(self):

        try:
            codigo = self.entrada_codigo.get()
            nome = self.entrada_nome.get()

            if self.codigo_selecionado is None:

                disciplina = Disciplina(codigo, nome)

                self.gerenciamento.cadastrar_disciplina(disciplina)

                messagebox.showinfo(
                    "Sucesso",
                    "Disciplina cadastrada com sucesso."
                )

            else:

                self.gerenciamento.editar_disciplina(
                    self.codigo_selecionado,
                    novo_codigo=codigo,
                    novo_nome=nome
                )

                messagebox.showinfo(
                    "Sucesso",
                    "Dados da disciplina atualizados com sucesso."
                )

            self.limpar_formulario()
            self.atualizar_lista()

        except (ValueError, TypeError) as erro:
            messagebox.showerror("Erro", str(erro))

    def selecionar_disciplina(self, disciplina):

        self.limpar_formulario()

        self.entrada_codigo.insert(0, disciplina.get_codigo())
        self.entrada_nome.insert(0, disciplina.get_nome())

        self.codigo_selecionado = disciplina.get_codigo()

        self.botao_salvar.configure(text="Salvar alterações")

    def excluir_disciplina(self, codigo):

        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            "Deseja realmente excluir esta disciplina?"
        )

        if confirmar:

            try:
                self.gerenciamento.excluir_disciplina(codigo)

                messagebox.showinfo(
                    "Sucesso",
                    "Disciplina excluída com sucesso."
                )

                if self.codigo_selecionado == codigo:
                    self.limpar_formulario()

                self.atualizar_lista()

            except (ValueError, TypeError) as erro:
                messagebox.showerror("Erro", str(erro))

    def limpar_formulario(self):

        self.entrada_codigo.delete(0, "end")
        self.entrada_nome.delete(0, "end")

        self.codigo_selecionado = None

        self.botao_salvar.configure(text="Cadastrar disciplina")

    def atualizar_lista(self):

        for widget in self.lista_disciplinas.winfo_children():
            widget.destroy()

        disciplinas = self.gerenciamento.listar_disciplinas()

        if not disciplinas:

            mensagem = ctk.CTkLabel(
                self.lista_disciplinas,
                text="Nenhuma disciplina cadastrada.",
                font=("Arial", 14),
                text_color="#64748B"
            )

            mensagem.pack(pady=25)
            return

        for disciplina in disciplinas:

            linha = ctk.CTkFrame(
                self.lista_disciplinas,
                fg_color="#F8FAFC",
                corner_radius=8
            )

            linha.pack(fill="x", padx=8, pady=5)

            informacoes = (
                f"{disciplina.get_nome()} | "
                f"Código: {disciplina.get_codigo()}"
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
                command=lambda codigo=disciplina.get_codigo(): self.excluir_disciplina(codigo)
            ).pack(side="right", padx=10, pady=8)

            ctk.CTkButton(
                linha,
                text="Editar",
                width=80,
                fg_color="#6D28D9",
                hover_color="#5B21B6",
                command=lambda materia=disciplina: self.selecionar_disciplina(materia)
            ).pack(side="right", padx=5, pady=8)
            
  