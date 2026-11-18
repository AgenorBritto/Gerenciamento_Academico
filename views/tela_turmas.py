
import customtkinter as ctk
from tkinter import messagebox

from models.turma import Turma


class TelaTurmas(ctk.CTkFrame):

    def __init__(self, master, gerenciamento):
        super().__init__(master, fg_color="transparent")

        self.gerenciamento = gerenciamento
        self.codigo_selecionado = None

        self.criar_interface()
        self.atualizar_lista()

    def criar_interface(self):

        # Cabeçalho
        cabecalho = ctk.CTkFrame(self, fg_color="transparent")
        cabecalho.pack(fill="x", pady=(0, 20))

        ctk.CTkLabel(
            cabecalho,
            text="Gerenciamento de Turmas",
            font=("Arial", 26, "bold"),
            text_color="#1E293B"
        ).pack(anchor="w")

        ctk.CTkLabel(
            cabecalho,
            text="Cadastre e gerencie as turmas de ingresso dos alunos.",
            font=("Arial", 14),
            text_color="#64748B"
        ).pack(anchor="w", pady=(5, 0))

        # Formulário
        self.formulario = ctk.CTkFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#E2E8F0"
        )

        self.formulario.pack(fill="x", pady=(0, 20))
        self.formulario.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(
            self.formulario,
            text="Dados da turma",
            font=("Arial", 18, "bold"),
            text_color="#1E293B"
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(20, 15))

        # Código
        ctk.CTkLabel(
            self.formulario,
            text="Código da turma",
            text_color="#334155"
        ).grid(row=1, column=0, sticky="w", padx=20)

        self.campo_codigo = ctk.CTkEntry(
            self.formulario,
            placeholder_text="Ex: ADS-2026-A",
            height=38
        )

        self.campo_codigo.grid(row=2, column=0, sticky="ew", padx=20, pady=(5, 12))

        # Curso
        ctk.CTkLabel(
            self.formulario,
            text="Curso",
            text_color="#334155"
        ).grid(row=1, column=1, sticky="w", padx=20)

        self.campo_curso = ctk.CTkEntry(
            self.formulario,
            placeholder_text="Ex: Análise e Desenvolvimento de Sistemas",
            height=38
        )

        self.campo_curso.grid(row=2, column=1, sticky="ew", padx=20, pady=(5, 12))

        # Período de ingresso
        ctk.CTkLabel(
            self.formulario,
            text="Período de ingresso",
            text_color="#334155"
        ).grid(row=3, column=0, sticky="w", padx=20)

        self.campo_periodo = ctk.CTkEntry(
            self.formulario,
            placeholder_text="Ex: 2026.1",
            height=38
        )

        self.campo_periodo.grid(row=4, column=0, sticky="ew", padx=20, pady=(5, 12))

        # Limite de alunos
        ctk.CTkLabel(
            self.formulario,
            text="Limite de alunos",
            text_color="#334155"
        ).grid(row=3, column=1, sticky="w", padx=20)

        self.campo_limite = ctk.CTkEntry(
            self.formulario,
            placeholder_text="Ex: 40",
            height=38
        )

        self.campo_limite.insert(0, "40")
        self.campo_limite.grid(row=4, column=1, sticky="ew", padx=20, pady=(5, 12))

        # Botões
        botoes = ctk.CTkFrame(self.formulario, fg_color="transparent")
        botoes.grid(row=5, column=0, columnspan=2, sticky="w", padx=20, pady=(5, 20))

        ctk.CTkButton(
            botoes,
            text="Cadastrar turma",
            width=140,
            height=38,
            fg_color="#6D28D9",
            hover_color="#5B21B6",
            command=self.cadastrar_turma
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            botoes,
            text="Salvar edição",
            width=120,
            height=38,
            fg_color="#2563EB",
            hover_color="#1D4ED8",
            command=self.editar_turma
        ).pack(side="left", padx=8)

        ctk.CTkButton(
            botoes,
            text="Limpar",
            width=90,
            height=38,
            fg_color="#64748B",
            hover_color="#475569",
            command=self.limpar_campos
        ).pack(side="left", padx=8)

        # Lista de turmas
        ctk.CTkLabel(
            self,
            text="Turmas cadastradas",
            font=("Arial", 19, "bold"),
            text_color="#1E293B"
        ).pack(anchor="w", pady=(5, 10))

        self.lista_turmas = ctk.CTkScrollableFrame(
            self,
            fg_color="transparent",
            corner_radius=8
        )

        self.lista_turmas.pack(fill="both", expand=True)

    def cadastrar_turma(self):

        try:
            codigo = self.campo_codigo.get().strip()
            curso = self.campo_curso.get().strip()
            periodo = self.campo_periodo.get().strip()
            limite = int(self.campo_limite.get())

            turma = Turma(codigo, curso, periodo, limite)

            self.gerenciamento.cadastrar_turma(turma)

            messagebox.showinfo(
                "Sucesso",
                "Turma cadastrada com sucesso!"
            )

            self.limpar_campos()
            self.atualizar_lista()

        except ValueError as erro:
            messagebox.showerror("Erro", str(erro))

        except Exception as erro:
            messagebox.showerror("Erro", str(erro))

    def editar_turma(self):

        if self.codigo_selecionado is None:
            messagebox.showwarning(
                "Atenção",
                "Selecione uma turma para editar."
            )
            return

        try:
            codigo = self.campo_codigo.get().strip()
            curso = self.campo_curso.get().strip()
            periodo = self.campo_periodo.get().strip()
            limite = int(self.campo_limite.get())

            self.gerenciamento.editar_turma(
                self.codigo_selecionado,
                novo_codigo=codigo,
                novo_curso=curso,
                novo_periodo=periodo,
                novo_limite=limite
            )

            messagebox.showinfo(
                "Sucesso",
                "Turma atualizada com sucesso!"
            )

            self.limpar_campos()
            self.atualizar_lista()

        except ValueError as erro:
            messagebox.showerror("Erro", str(erro))

        except Exception as erro:
            messagebox.showerror("Erro", str(erro))

    def excluir_turma(self, codigo):

        resposta = messagebox.askyesno(
            "Confirmar exclusão",
            f"Deseja realmente excluir a turma {codigo}?"
        )

        if not resposta:
            return

        try:
            self.gerenciamento.excluir_turma(codigo)

            messagebox.showinfo(
                "Sucesso",
                "Turma excluída com sucesso!"
            )

            self.limpar_campos()
            self.atualizar_lista()

        except Exception as erro:
            messagebox.showerror("Erro", str(erro))

    
    def selecionar_turma(self, turma):

        self.limpar_campos()

        self.campo_codigo.insert(0, turma.get_codigo())
        self.campo_curso.insert(0, turma.get_curso())
        self.campo_periodo.insert(0, turma.get_periodo_ingresso())
        self.campo_limite.delete(0, "end")
        self.campo_limite.insert(0, str(turma.get_limite_alunos()))

        self.codigo_selecionado = turma.get_codigo()

    def limpar_campos(self):

        self.codigo_selecionado = None

        self.campo_codigo.delete(0, "end")
        self.campo_curso.delete(0, "end")
        self.campo_periodo.delete(0, "end")
        self.campo_limite.delete(0, "end")

        self.campo_limite.insert(0, "40")

    def atualizar_lista(self):

        for widget in self.lista_turmas.winfo_children():
            widget.destroy()

        turmas = self.gerenciamento.listar_turmas()

        if not turmas:

            ctk.CTkLabel(
                self.lista_turmas,
                text="Nenhuma turma cadastrada.",
                font=("Arial", 14),
                text_color="#64748B"
            ).pack(pady=20)

            return

        for turma in turmas:

            quantidade_alunos = sum(
                1 for aluno in self.gerenciamento.listar_alunos()
                if aluno.get_turma() is turma
            )

            card = ctk.CTkFrame(
                self.lista_turmas,
                fg_color="#FFFFFF",
                corner_radius=10,
                border_width=1,
                border_color="#E2E8F0"
            )

            card.pack(fill="x", pady=5, padx=2)

            informacoes = ctk.CTkFrame(card, fg_color="transparent")
            informacoes.pack(side="left", fill="both", expand=True, padx=15, pady=12)

            ctk.CTkLabel(
                informacoes,
                text=f"{turma.get_codigo()} - {turma.get_curso()}",
                font=("Arial", 15, "bold"),
                text_color="#1E293B"
            ).pack(anchor="w")

            ctk.CTkLabel(
                informacoes,
                text=f"Ingresso: {turma.get_periodo_ingresso()} | "
                     f"Alunos: {quantidade_alunos}/{turma.get_limite_alunos()}",
                font=("Arial", 12),
                text_color="#64748B"
            ).pack(anchor="w", pady=(4, 0))

            botoes = ctk.CTkFrame(card, fg_color="transparent")
            botoes.pack(side="right", padx=10)

            ctk.CTkButton(
                botoes,
                text="Selecionar",
                width=90,
                height=32,
                fg_color="#6D28D9",
                hover_color="#5B21B6",
                command=lambda t=turma: self.selecionar_turma(t)
            ).pack(pady=3)

            ctk.CTkButton(
                botoes,
                text="Excluir",
                width=90,
                height=32,
                fg_color="#DC2626",
                hover_color="#B91C1C",
                command=lambda c=turma.get_codigo(): self.excluir_turma(c)
            ).pack(pady=3)
