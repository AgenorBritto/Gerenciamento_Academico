
import customtkinter as ctk
from tkinter import messagebox

from models.professor import Professor


class TelaProfessores(ctk.CTkFrame):

    def __init__(self, master, gerenciamento, gerenciamento_professores):
        super().__init__(master, fg_color="transparent")

        self.gerenciamento = gerenciamento
        self.gerenciamento_professores = gerenciamento_professores
        self.codigo_selecionado = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.criar_titulo()
        self.criar_formulario()
        self.criar_lista()

        self.atualizar_lista()

    def criar_titulo(self):

        titulo = ctk.CTkLabel(self, text="Gerenciamento de Professores", font=("Arial", 26, "bold"), text_color="#1E293B")
        titulo.grid(row=0, column=0, sticky="w", pady=(10, 5))

        descricao = ctk.CTkLabel(self, text="Cadastre, consulte, edite ou exclua professores do sistema.", font=("Arial", 14), text_color="#64748B")
        descricao.grid(row=1, column=0, sticky="w", pady=(0, 20))

    def criar_formulario(self):

        formulario = ctk.CTkFrame(self, fg_color="#FFFFFF", corner_radius=12, border_width=1, border_color="#E2E8F0")
        formulario.grid(row=2, column=0, sticky="new", pady=(0, 20))
        formulario.grid_columnconfigure((0, 1), weight=1)

        titulo = ctk.CTkLabel(formulario, text="Dados do professor", font=("Arial", 18, "bold"), text_color="#1E293B")
        titulo.grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(20, 15))

        ctk.CTkLabel(formulario, text="Nome", text_color="#334155").grid(row=1, column=0, sticky="w", padx=20)
        ctk.CTkLabel(formulario, text="Idade", text_color="#334155").grid(row=1, column=1, sticky="w", padx=20)

        self.entrada_nome = ctk.CTkEntry(formulario, placeholder_text="Nome completo", height=38)
        self.entrada_nome.grid(row=2, column=0, sticky="ew", padx=20, pady=(5, 15))

        self.entrada_idade = ctk.CTkEntry(formulario, placeholder_text="Idade", height=38)
        self.entrada_idade.grid(row=2, column=1, sticky="ew", padx=20, pady=(5, 15))

        ctk.CTkLabel(formulario, text="Código", text_color="#334155").grid(row=3, column=0, sticky="w", padx=20)
        ctk.CTkLabel(formulario, text="Especialidade", text_color="#334155").grid(row=3, column=1, sticky="w", padx=20)

        self.entrada_codigo = ctk.CTkEntry(formulario, placeholder_text="Ex.: P001", height=38)
        self.entrada_codigo.grid(row=4, column=0, sticky="ew", padx=20, pady=(5, 15))

        self.entrada_especialidade = ctk.CTkEntry(formulario, placeholder_text="Ex.: Matemática", height=38)
        self.entrada_especialidade.grid(row=4, column=1, sticky="ew", padx=20, pady=(5, 15))

        ctk.CTkLabel(formulario, text="Usuário de acesso", text_color="#334155").grid(row=5, column=0, sticky="w", padx=20)
        ctk.CTkLabel(formulario, text="Senha de acesso", text_color="#334155").grid(row=5, column=1, sticky="w", padx=20)

        self.entrada_usuario = ctk.CTkEntry(formulario, placeholder_text="Nome de usuário", height=38)
        self.entrada_usuario.grid(row=6, column=0, sticky="ew", padx=20, pady=(5, 20))

        self.entrada_senha = ctk.CTkEntry(formulario, placeholder_text="Mínimo de 6 caracteres", show="*", height=38)
        self.entrada_senha.grid(row=6, column=1, sticky="ew", padx=20, pady=(5, 20))

        botoes = ctk.CTkFrame(formulario, fg_color="transparent")
        botoes.grid(row=7, column=0, columnspan=2, sticky="w", padx=20, pady=(0, 20))

        self.botao_salvar = ctk.CTkButton(botoes, text="Cadastrar professor", width=170, height=38, fg_color="#6D28D9", hover_color="#5B21B6", command=self.salvar_professor)
        self.botao_salvar.pack(side="left", padx=(0, 10))

        ctk.CTkButton(botoes, text="Limpar", width=100, height=38, fg_color="#E2E8F0", hover_color="#CBD5E1", text_color="#334155", command=self.limpar_formulario).pack(side="left")

    def criar_lista(self):

        titulo = ctk.CTkLabel(self, text="Professores cadastrados", font=("Arial", 18, "bold"), text_color="#1E293B")
        titulo.grid(row=3, column=0, sticky="w", pady=(0, 10))

        self.lista_professores = ctk.CTkScrollableFrame(self, fg_color="#FFFFFF", corner_radius=12, border_width=1, border_color="#E2E8F0")
        self.lista_professores.grid(row=4, column=0, sticky="nsew")

    def salvar_professor(self):

        try:
            nome = self.entrada_nome.get()
            idade = int(self.entrada_idade.get())
            codigo = self.entrada_codigo.get()
            especialidade = self.entrada_especialidade.get()
            usuario = self.entrada_usuario.get()
            senha = self.entrada_senha.get()

            if self.codigo_selecionado is None:
                professor = Professor(nome, idade, codigo, especialidade)

                self.gerenciamento_professores.cadastrar_professor(
                    professor,
                    usuario,
                    senha
                )

                messagebox.showinfo("Sucesso", "Professor cadastrado com sucesso.")

            else:
                self.gerenciamento_professores.editar_professor(
                    self.codigo_selecionado,
                    novo_nome=nome,
                    nova_idade=idade,
                    novo_codigo=codigo,
                    nova_especialidade=especialidade,
                    novo_usuario=usuario,
                    nova_senha=senha
                )

                messagebox.showinfo("Sucesso", "Dados do professor atualizados com sucesso.")

            self.limpar_formulario()
            self.atualizar_lista()

        except (ValueError, TypeError) as erro:
            messagebox.showerror("Erro", str(erro))

    def selecionar_professor(self, professor):

        self.limpar_formulario()

        self.entrada_nome.insert(0, professor.get_nome())
        self.entrada_idade.insert(0, str(professor.get_idade()))
        self.entrada_codigo.insert(0, professor.get_codigo())
        self.entrada_especialidade.insert(0, professor.get_especialidade())

        usuario = self.gerenciamento_professores.obter_usuario(professor.get_codigo())

        if usuario is not None:
            self.entrada_usuario.insert(0, usuario)

        self.codigo_selecionado = professor.get_codigo()

        self.botao_salvar.configure(text="Salvar alterações")

    def excluir_professor(self, codigo):

        confirmar = messagebox.askyesno("Confirmar exclusão", "Deseja realmente excluir este professor?")

        if confirmar:
            try:
                self.gerenciamento_professores.excluir_professor(codigo)
                messagebox.showinfo("Sucesso", "Professor excluído com sucesso.")

                if self.codigo_selecionado == codigo:
                    self.limpar_formulario()

                self.atualizar_lista()

            except (ValueError, TypeError) as erro:
                messagebox.showerror("Erro", str(erro))

    def limpar_formulario(self):

        self.entrada_nome.delete(0, "end")
        self.entrada_idade.delete(0, "end")
        self.entrada_codigo.delete(0, "end")
        self.entrada_especialidade.delete(0, "end")
        self.entrada_usuario.delete(0, "end")
        self.entrada_senha.delete(0, "end")

        self.codigo_selecionado = None
        self.botao_salvar.configure(text="Cadastrar professor")

    def atualizar_lista(self):

        for widget in self.lista_professores.winfo_children():
            widget.destroy()

        professores = self.gerenciamento.listar_professores()

        if not professores:
            mensagem = ctk.CTkLabel(self.lista_professores, text="Nenhum professor cadastrado.", font=("Arial", 14), text_color="#64748B")
            mensagem.pack(pady=25)
            return

        for professor in professores:
            linha = ctk.CTkFrame(self.lista_professores, fg_color="#F8FAFC", corner_radius=8)
            linha.pack(fill="x", padx=8, pady=5)

            usuario = self.gerenciamento_professores.obter_usuario(professor.get_codigo())

            informacoes = (
                f"{professor.get_nome()} | "
                f"Código: {professor.get_codigo()} | "
                f"Especialidade: {professor.get_especialidade()} | "
                f"Usuário: {usuario if usuario else 'Sem acesso'}"
            )

            ctk.CTkLabel(linha, text=informacoes, font=("Arial", 13), text_color="#334155").pack(side="left", padx=15, pady=15)

            ctk.CTkButton(linha, text="Excluir", width=80, fg_color="#DC2626", hover_color="#B91C1C", command=lambda codigo=professor.get_codigo(): self.excluir_professor(codigo)).pack(side="right", padx=10, pady=8)

            ctk.CTkButton(linha, text="Editar", width=80, fg_color="#6D28D9", hover_color="#5B21B6", command=lambda docente=professor: self.selecionar_professor(docente)).pack(side="right", padx=5, pady=8)
