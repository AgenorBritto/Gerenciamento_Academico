
import customtkinter as ctk


class TelaSituacao(ctk.CTkFrame):

    def __init__(self, master, gerenciamento):
        super().__init__(master, fg_color="transparent")

        self.gerenciamento = gerenciamento
        self.disciplina_selecionada = None
        self.oferta_selecionada = None

        self.disciplinas_por_opcao = {}
        self.ofertas_por_opcao = {}

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)

        self.criar_titulo()
        self.criar_indicadores()
        self.criar_lista()
        self.atualizar_filtros()
        self.atualizar_dados()

    def criar_titulo(self):

        titulo = ctk.CTkLabel(
            self,
            text="Situação Acadêmica",
            font=("Arial", 26, "bold"),
            text_color="#1E293B"
        )
        titulo.grid(row=0, column=0, sticky="w", pady=(10, 5))

        descricao = ctk.CTkLabel(
            self,
            text="Acompanhe as médias e a situação dos alunos em cada disciplina.",
            font=("Arial", 14),
            text_color="#64748B"
        )
        descricao.grid(row=1, column=0, sticky="w", pady=(0, 20))

    def criar_indicadores(self):

        indicadores = ctk.CTkFrame(self, fg_color="transparent")
        indicadores.grid(row=2, column=0, sticky="ew", pady=(0, 15))
        indicadores.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.valor_total = self.criar_card(indicadores, "Matrículas", "0", 0)
        self.valor_aprovados = self.criar_card(indicadores, "Aprovados", "0", 1)
        self.valor_reprovados = self.criar_card(indicadores, "Reprovados", "0", 2)
        self.valor_sem_notas = self.criar_card(indicadores, "Sem notas", "0", 3)

    def criar_card(self, master, titulo, valor, coluna):

        card = ctk.CTkFrame(
            master,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#E2E8F0"
        )
        card.grid(row=0, column=coluna, sticky="nsew", padx=5)

        ctk.CTkLabel(
            card,
            text=titulo,
            font=("Arial", 12),
            text_color="#64748B"
        ).pack(anchor="w", padx=15, pady=(15, 5))

        resultado = ctk.CTkLabel(
            card,
            text=valor,
            font=("Arial", 24, "bold"),
            text_color="#6D28D9"
        )
        resultado.pack(anchor="w", padx=15, pady=(0, 15))

        return resultado

    def criar_lista(self):

        cabecalho = ctk.CTkFrame(self, fg_color="transparent")
        cabecalho.grid(row=3, column=0, sticky="ew", pady=(0, 10))
        cabecalho.grid_columnconfigure(0, weight=1)

        titulo = ctk.CTkLabel(
            cabecalho,
            text="Desempenho dos alunos",
            font=("Arial", 18, "bold"),
            text_color="#1E293B"
        )
        titulo.grid(row=0, column=0, sticky="w")

        ctk.CTkButton(
            cabecalho,
            text="Atualizar dados",
            width=130,
            height=32,
            fg_color="#6D28D9",
            hover_color="#5B21B6",
            command=self.atualizar_tela
        ).grid(row=0, column=1, sticky="e")

        filtros = ctk.CTkFrame(self, fg_color="transparent")
        filtros.grid(row=4, column=0, sticky="ew", pady=(0, 12))
        filtros.grid_columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(
            filtros,
            text="Disciplina",
            font=("Arial", 12),
            text_color="#64748B"
        ).grid(row=0, column=0, sticky="w", padx=5)

        ctk.CTkLabel(
            filtros,
            text="Oferta",
            font=("Arial", 12),
            text_color="#64748B"
        ).grid(row=0, column=1, sticky="w", padx=5)

        self.filtro_disciplina = ctk.CTkOptionMenu(
            filtros,
            values=["Todas as disciplinas"],
            command=self.filtrar_disciplina,
            fg_color="#6D28D9",
            button_color="#5B21B6",
            button_hover_color="#4C1D95",
            height=36
        )
        self.filtro_disciplina.grid(
            row=1, column=0, sticky="ew", padx=5, pady=(5, 0)
        )

        self.filtro_oferta = ctk.CTkOptionMenu(
            filtros,
            values=["Todas as ofertas"],
            command=self.filtrar_oferta,
            fg_color="#6D28D9",
            button_color="#5B21B6",
            button_hover_color="#4C1D95",
            height=36
        )
        self.filtro_oferta.grid(
            row=1, column=1, sticky="ew", padx=5, pady=(5, 0)
        )

        self.lista_situacao = ctk.CTkScrollableFrame(
            self,
            fg_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#E2E8F0"
        )
        self.lista_situacao.grid(row=5, column=0, sticky="nsew")

    def atualizar_filtros(self):

        disciplinas = self.gerenciamento.listar_disciplinas()

        self.disciplinas_por_opcao = {}

        opcoes_disciplinas = ["Todas as disciplinas"]

        for disciplina in disciplinas:
            opcao = f"{disciplina.get_codigo()} - {disciplina.get_nome()}"
            opcoes_disciplinas.append(opcao)
            self.disciplinas_por_opcao[opcao] = disciplina

        self.filtro_disciplina.configure(values=opcoes_disciplinas)
        self.filtro_disciplina.set("Todas as disciplinas")

        self.atualizar_opcoes_ofertas()

    def atualizar_opcoes_ofertas(self):

        ofertas = self.gerenciamento.listar_ofertas()

        self.ofertas_por_opcao = {}

        opcoes_ofertas = ["Todas as ofertas"]

        for oferta in ofertas:

            if (
                self.disciplina_selecionada is not None
                and oferta.get_disciplina() is not self.disciplina_selecionada
            ):
                continue

            opcao = (
                f"{oferta.get_codigo()} - "
                f"{oferta.get_disciplina().get_nome()} - "
                f"Seção {oferta.get_codigo_turma()}"
            )

            opcoes_ofertas.append(opcao)
            self.ofertas_por_opcao[opcao] = oferta

        self.filtro_oferta.configure(values=opcoes_ofertas)
        self.filtro_oferta.set("Todas as ofertas")

    def filtrar_disciplina(self, opcao):

        self.disciplina_selecionada = self.disciplinas_por_opcao.get(opcao)

        self.oferta_selecionada = None

        self.atualizar_opcoes_ofertas()
        self.atualizar_dados()

    def filtrar_oferta(self, opcao):

        self.oferta_selecionada = self.ofertas_por_opcao.get(opcao)

        self.atualizar_dados()

    def atualizar_tela(self):

        self.disciplina_selecionada = None
        self.oferta_selecionada = None
        self.atualizar_filtros()
        self.atualizar_dados()

    def atualizar_dados(self):

        for widget in self.lista_situacao.winfo_children():
            widget.destroy()

        matriculas = self.gerenciamento.listar_matriculas()

        if self.disciplina_selecionada is not None:
            matriculas = [
                matricula for matricula in matriculas
                if matricula.get_oferta().get_disciplina() is self.disciplina_selecionada
            ]

        if self.oferta_selecionada is not None:
            matriculas = [
                matricula for matricula in matriculas
                if matricula.get_oferta() is self.oferta_selecionada
            ]

        total = len(matriculas)
        aprovados = 0
        reprovados = 0
        sem_notas = 0

        if not matriculas:
            mensagem = ctk.CTkLabel(
                self.lista_situacao,
                text="Nenhuma matrícula encontrada para os filtros selecionados.",
                font=("Arial", 14),
                text_color="#64748B"
            )
            mensagem.pack(pady=25)

        for matricula in matriculas:

            aluno = matricula.get_aluno()
            oferta = matricula.get_oferta()
            disciplina = oferta.get_disciplina()

            codigo_oferta = oferta.get_codigo()
            codigo_aluno = aluno.get_matricula()

            media = self.gerenciamento.consultar_media(
                codigo_aluno, codigo_oferta
            )

            situacao = self.gerenciamento.consultar_situacao(
                codigo_aluno, codigo_oferta
            )

            quantidade = len(matricula.listar_avaliacoes())

            if situacao == "Aprovado":
                aprovados += 1
            elif situacao == "Reprovado":
                reprovados += 1
            else:
                sem_notas += 1

            self.criar_linha(
                aluno,
                oferta,
                disciplina,
                media,
                situacao,
                quantidade
            )

        self.valor_total.configure(text=str(total))
        self.valor_aprovados.configure(text=str(aprovados))
        self.valor_reprovados.configure(text=str(reprovados))
        self.valor_sem_notas.configure(text=str(sem_notas))

    def criar_linha(self, aluno, oferta, disciplina, media, situacao, quantidade):

        linha = ctk.CTkFrame(
            self.lista_situacao,
            fg_color="#F8FAFC",
            corner_radius=8
        )
        linha.pack(fill="x", padx=8, pady=5)

        informacoes = ctk.CTkFrame(linha, fg_color="transparent")
        informacoes.pack(side="left", fill="x", expand=True, padx=15, pady=12)

        ctk.CTkLabel(
            informacoes,
            text=aluno.get_nome(),
            font=("Arial", 14, "bold"),
            text_color="#1E293B"
        ).pack(anchor="w")

        detalhes = (
            f"Matrícula: {aluno.get_matricula()} | "
            f"Disciplina: {disciplina.get_nome()}"
        )

        ctk.CTkLabel(
            informacoes,
            text=detalhes,
            font=("Arial", 12),
            text_color="#64748B"
        ).pack(anchor="w", pady=(3, 0))

        detalhes_oferta = (
            f"Professor: {oferta.get_professor().get_nome()} | "
            f"Seção: {oferta.get_codigo_turma()} | "
            f"Período: {oferta.get_periodo()}"
        )

        ctk.CTkLabel(
            informacoes,
            text=detalhes_oferta,
            font=("Arial", 11),
            text_color="#64748B"
        ).pack(anchor="w", pady=(3, 0))

        resultado = ctk.CTkFrame(linha, fg_color="transparent")
        resultado.pack(side="right", padx=15, pady=10)

        ctk.CTkLabel(
            resultado,
            text=f"Média: {media:.2f}",
            font=("Arial", 13, "bold"),
            text_color="#6D28D9"
        ).pack(anchor="e")

        texto_situacao = f"{situacao} | {quantidade} avaliação(ões)"
        cor = "#64748B"

        if situacao == "Aprovado":
            cor = "#15803D"
        elif situacao == "Reprovado":
            cor = "#DC2626"

        ctk.CTkLabel(
            resultado,
            text=texto_situacao,
            font=("Arial", 12),
            text_color=cor
        ).pack(anchor="e", pady=(3, 0))
