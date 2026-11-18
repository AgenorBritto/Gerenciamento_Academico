from models.aluno import Aluno
from models.professor import Professor
from models.disciplina import Disciplina
from models.matricula import Matricula
from models.turma import Turma
from models.oferta_disciplina import OfertaDisciplina


class GerenciamentoAcademico:

    def __init__(self):
        self._alunos = []
        self._professores = []
        self._disciplinas = []
        self._matriculas = []
        self._turmas = []
        self._ofertas = []


    # ==================================
    # GERENCIAMENTO DE TURMAS DE INGRESSO
    # ==================================

    def cadastrar_turma(self, turma):

        if not isinstance(turma, Turma):
            raise TypeError("É necessário informar um objeto Turma.")

        if self.buscar_turma(turma.get_codigo()):
            raise ValueError("Código de turma já cadastrado.")

        self._turmas.append(turma)
        return turma

    def buscar_turma(self, codigo):

        for turma in self._turmas:
            if turma.get_codigo() == codigo:
                return turma

        return None

    def listar_turmas(self):
        return self._turmas.copy()

    def editar_turma(self, codigo_atual, novo_codigo=None, novo_curso=None, novo_periodo=None, novo_limite=None):

        turma = self.buscar_turma(codigo_atual)

        if turma is None:
            raise ValueError("Turma não encontrada.")

        codigo = turma.get_codigo() if novo_codigo is None else novo_codigo
        curso = turma.get_curso() if novo_curso is None else novo_curso
        periodo = turma.get_periodo_ingresso() if novo_periodo is None else novo_periodo
        limite = turma.get_limite_alunos() if novo_limite is None else novo_limite

        outra_turma = self.buscar_turma(codigo)

        if outra_turma is not None and outra_turma is not turma:
            raise ValueError("Código já cadastrado por outra turma.")

        turma_validacao = Turma(codigo, curso, periodo, limite)

        quantidade_alunos = sum(1 for aluno in self._alunos if aluno.get_turma() is turma)

        if turma_validacao.get_limite_alunos() < quantidade_alunos:
            raise ValueError("O limite não pode ser menor que a quantidade de alunos da turma.")

        turma.set_codigo(turma_validacao.get_codigo())
        turma.set_curso(turma_validacao.get_curso())
        turma.set_periodo_ingresso(turma_validacao.get_periodo_ingresso())
        turma.set_limite_alunos(turma_validacao.get_limite_alunos())

        return turma

    def excluir_turma(self, codigo):

        turma = self.buscar_turma(codigo)

        if turma is None:
            raise ValueError("Turma não encontrada.")

        for aluno in self._alunos:
            if aluno.get_turma() is turma:
                raise ValueError("Não é possível excluir: existem alunos vinculados à turma.")

        self._turmas.remove(turma)
        return turma


    # ==================================
    # GERENCIAMENTO DE ALUNOS
    # ==================================

    
    def cadastrar_aluno(self, aluno):

        if not isinstance(aluno, Aluno):
            raise TypeError("É necessário informar um objeto Aluno.")

        if self.buscar_aluno(aluno.get_matricula()):
            raise ValueError("Matrícula já cadastrada.")

        turma = aluno.get_turma()

        if self.buscar_turma(turma.get_codigo()) is not turma:
            raise ValueError("Turma não cadastrada no sistema.")

        quantidade_alunos = sum(1 for a in self._alunos if a.get_turma() is turma)

        if quantidade_alunos >= turma.get_limite_alunos():
            raise ValueError("Não há vagas disponíveis nesta turma.")

        self._alunos.append(aluno)
        return aluno


    def buscar_aluno(self, matricula):

        for aluno in self._alunos:
            if aluno.get_matricula() == matricula:
                return aluno

        return None

    def listar_alunos(self):
        return self._alunos.copy()

    
    def editar_aluno(
        self,
        matricula_atual,
        novo_nome=None,
        nova_idade=None,
        nova_matricula=None,
        nova_turma=None
    ):

        aluno = self.buscar_aluno(matricula_atual)

        if aluno is None:
            raise ValueError("Aluno não encontrado.")

        # Define os valores: mantém os atuais quando não informados
        nome = aluno.get_nome() if novo_nome is None else novo_nome
        idade = aluno.get_idade() if nova_idade is None else nova_idade
        matricula = (
            aluno.get_matricula()
            if nova_matricula is None
            else nova_matricula
        )
        turma = aluno.get_turma() if nova_turma is None else nova_turma
        
        if not isinstance(turma, Turma):
            raise TypeError("É necessário informar um objeto Turma.")

        if self.buscar_turma(turma.get_codigo()) is not turma:
            raise ValueError("Turma não cadastrada no sistema.")

        quantidade_alunos = sum(1 for a in self._alunos if a.get_turma() is turma and a is not aluno)

        if quantidade_alunos >= turma.get_limite_alunos():
            raise ValueError("Não há vagas disponíveis nesta turma.")

        # Verifica se a nova matrícula pertence a outro aluno
        outro_aluno = self.buscar_aluno(matricula)

        if outro_aluno is not None and outro_aluno is not aluno:
            raise ValueError("Matrícula já cadastrada por outro aluno.")

        # Valida todos os dados antes de alterar o objeto original
        aluno_validacao = Aluno(nome, idade, matricula, turma)

        # Aplica as alterações após a validação
        aluno.set_nome(aluno_validacao.get_nome())
        aluno.set_idade(aluno_validacao.get_idade())
        aluno.set_matricula(aluno_validacao.get_matricula())
        aluno.set_turma(aluno_validacao.get_turma())

        return aluno


    
    def excluir_aluno(self, matricula):

        aluno = self.buscar_aluno(matricula)

        if aluno is None:
            raise ValueError("Aluno não encontrado.")

        matriculas_aluno = [
            m for m in self._matriculas
            if m.get_aluno() is aluno
        ]

        for m in matriculas_aluno:
            if m.listar_avaliacoes():
                raise ValueError(
                    "Não é possível excluir este aluno: existem avaliações registradas no seu histórico acadêmico."
                )

        for m in matriculas_aluno:
            self._matriculas.remove(m)

        self._alunos.remove(aluno)
        return aluno


    # ==================================
    # GERENCIAMENTO DE PROFESSORES
    # ==================================

    def cadastrar_professor(self, professor):

        if not isinstance(professor, Professor):
            raise TypeError("É necessário informar um objeto Professor.")

        if self.buscar_professor(professor.get_codigo()):
            raise ValueError("Código de professor já cadastrado.")

        self._professores.append(professor)
        return professor

    def buscar_professor(self, codigo):

        for professor in self._professores:
            if professor.get_codigo() == codigo:
                return professor

        return None

    def listar_professores(self):
        return self._professores.copy()

    
    def editar_professor(
        self,
        codigo_atual,
        novo_nome=None,
        nova_idade=None,
        novo_codigo=None,
        nova_especialidade=None
    ):

        professor = self.buscar_professor(codigo_atual)

        if professor is None:
            raise ValueError("Professor não encontrado.")

        # Mantém os valores atuais quando não forem informados
        nome = professor.get_nome() if novo_nome is None else novo_nome
        idade = professor.get_idade() if nova_idade is None else nova_idade

        codigo = (
            professor.get_codigo()
            if novo_codigo is None
            else novo_codigo
        )

        especialidade = (
            professor.get_especialidade()
            if nova_especialidade is None
            else nova_especialidade
        )

        # Verifica se o código pertence a outro professor
        outro_professor = self.buscar_professor(codigo)

        if outro_professor is not None and outro_professor is not professor:
            raise ValueError("Código já cadastrado por outro professor.")

        # Valida todos os dados antes de alterar o objeto original
        professor_validacao = Professor(
            nome,
            idade,
            codigo,
            especialidade
        )

        # Aplica as alterações após a validação
        professor.set_nome(professor_validacao.get_nome())
        professor.set_idade(professor_validacao.get_idade())
        professor.set_codigo(professor_validacao.get_codigo())
        professor.set_especialidade(
            professor_validacao.get_especialidade()
        )

        return professor


    def excluir_professor(self, codigo):

        professor = self.buscar_professor(codigo)

        if professor is None:
            raise ValueError("Professor não encontrado.")

        # Impede excluir professor que possui ofertas
        for oferta in self._ofertas:
            if oferta.get_professor() is professor:
                raise ValueError("Não é possível excluir: professor possui ofertas.")

        self._professores.remove(professor)
        return professor

    
    # ==================================
    # GERENCIAMENTO DE DISCIPLINAS
    # ==================================

    def cadastrar_disciplina(self, disciplina):

        if not isinstance(disciplina, Disciplina):
            raise TypeError("É necessário informar um objeto Disciplina.")

        if self.buscar_disciplina(disciplina.get_codigo()):
            raise ValueError("Código de disciplina já cadastrado.")

        self._disciplinas.append(disciplina)
        return disciplina

    def buscar_disciplina(self, codigo):

        for disciplina in self._disciplinas:
            if disciplina.get_codigo() == codigo:
                return disciplina

        return None

    def listar_disciplinas(self):
        return self._disciplinas.copy()

    def editar_disciplina(self, codigo_atual, novo_codigo=None, novo_nome=None):

        disciplina = self.buscar_disciplina(codigo_atual)

        if disciplina is None:
            raise ValueError("Disciplina não encontrada.")

        codigo = disciplina.get_codigo() if novo_codigo is None else novo_codigo
        nome = disciplina.get_nome() if novo_nome is None else novo_nome

        outra_disciplina = self.buscar_disciplina(codigo)

        if outra_disciplina is not None and outra_disciplina is not disciplina:
            raise ValueError("Código já cadastrado por outra disciplina.")

        disciplina_validacao = Disciplina(codigo, nome)

        disciplina.set_codigo(disciplina_validacao.get_codigo())
        disciplina.set_nome(disciplina_validacao.get_nome())

        return disciplina

    def excluir_disciplina(self, codigo):

        disciplina = self.buscar_disciplina(codigo)

        if disciplina is None:
            raise ValueError("Disciplina não encontrada.")

        for oferta in self._ofertas:
            if oferta.get_disciplina() is disciplina:
                raise ValueError("Não é possível excluir: disciplina possui ofertas.")

        self._disciplinas.remove(disciplina)
        return disciplina


    # ==================================
    # GERENCIAMENTO DE OFERTAS
    # ==================================

    def cadastrar_oferta(self, oferta):

        if not isinstance(oferta, OfertaDisciplina):
            raise TypeError("É necessário informar um objeto OfertaDisciplina.")

        if self.buscar_oferta(oferta.get_codigo()):
            raise ValueError("Código de oferta já cadastrado.")

        disciplina = oferta.get_disciplina()
        professor = oferta.get_professor()

        if self.buscar_disciplina(disciplina.get_codigo()) is not disciplina:
            raise ValueError("Disciplina não cadastrada no sistema.")

        if self.buscar_professor(professor.get_codigo()) is not professor:
            raise ValueError("Professor não cadastrado no sistema.")

        self._ofertas.append(oferta)
        return oferta

    def buscar_oferta(self, codigo):

        for oferta in self._ofertas:
            if oferta.get_codigo() == codigo:
                return oferta

        return None

    def listar_ofertas(self):
        return self._ofertas.copy()

    
    def editar_oferta(self, codigo_atual, novo_codigo=None, nova_disciplina=None, novo_professor=None, novo_codigo_turma=None, novo_periodo=None, novo_limite_vagas=None):

        oferta = self.buscar_oferta(codigo_atual)

        if oferta is None:
            raise ValueError("Oferta não encontrada.")

        codigo = oferta.get_codigo() if novo_codigo is None else novo_codigo
        disciplina = oferta.get_disciplina() if nova_disciplina is None else nova_disciplina
        professor = oferta.get_professor() if novo_professor is None else novo_professor
        codigo_turma = oferta.get_codigo_turma() if novo_codigo_turma is None else novo_codigo_turma
        periodo = oferta.get_periodo() if novo_periodo is None else novo_periodo
        limite_vagas = oferta.get_limite_vagas() if novo_limite_vagas is None else novo_limite_vagas

        outra_oferta = self.buscar_oferta(codigo)

        if outra_oferta is not None and outra_oferta is not oferta:
            raise ValueError("Código já cadastrado por outra oferta.")

        if not isinstance(disciplina, Disciplina):
            raise TypeError("É necessário informar um objeto Disciplina.")

        if not isinstance(professor, Professor):
            raise TypeError("É necessário informar um objeto Professor.")

        if self.buscar_disciplina(disciplina.get_codigo()) is not disciplina:
            raise ValueError("Disciplina não cadastrada no sistema.")

        if self.buscar_professor(professor.get_codigo()) is not professor:
            raise ValueError("Professor não cadastrado no sistema.")

        quantidade_matriculas = sum(
            1 for m in self._matriculas
            if m.get_oferta() is oferta
        )

        oferta_validacao = OfertaDisciplina(
            codigo,
            disciplina,
            professor,
            codigo_turma,
            periodo,
            limite_vagas
        )

        if oferta_validacao.get_limite_vagas() < quantidade_matriculas:
            raise ValueError("O limite de vagas não pode ser menor que a quantidade de alunos matriculados.")

        if quantidade_matriculas > 0:
            houve_alteracao = (
                codigo != oferta.get_codigo()
                or disciplina is not oferta.get_disciplina()
                or professor is not oferta.get_professor()
                or codigo_turma != oferta.get_codigo_turma()
                or periodo != oferta.get_periodo()
            )

            if houve_alteracao:
                raise ValueError("Não é possível alterar os dados principais de uma oferta que possui alunos matriculados.")

        oferta.set_codigo(oferta_validacao.get_codigo())
        oferta.set_disciplina(oferta_validacao.get_disciplina())
        oferta.set_professor(oferta_validacao.get_professor())
        oferta.set_codigo_turma(oferta_validacao.get_codigo_turma())
        oferta.set_periodo(oferta_validacao.get_periodo())
        oferta.set_limite_vagas(oferta_validacao.get_limite_vagas())

        return oferta

    def excluir_oferta(self, codigo):

        oferta = self.buscar_oferta(codigo)

        if oferta is None:
            raise ValueError("Oferta não encontrada.")

        for matricula in self._matriculas:
            if matricula.get_oferta() is oferta:
                raise ValueError("Não é possível excluir: oferta possui matrículas.")

        self._ofertas.remove(oferta)
        return oferta


    
    # ==================================
    # GERENCIAMENTO DE MATRÍCULAS
    # ==================================

    def matricular_aluno(self, matricula_aluno, codigo_oferta):

        aluno = self.buscar_aluno(matricula_aluno)
        oferta = self.buscar_oferta(codigo_oferta)

        if aluno is None:
            raise ValueError("Aluno não cadastrado no sistema.")

        if oferta is None:
            raise ValueError("Oferta não cadastrada no sistema.")

        disciplina = oferta.get_disciplina()

        # Impede matrícula duplicada na mesma disciplina
        for matricula in self._matriculas:
            if (
                matricula.get_aluno() is aluno
                and matricula.get_oferta().get_disciplina() is disciplina
            ):
                raise ValueError("Aluno já matriculado nesta disciplina.")

        # Verifica o limite de vagas da oferta
        quantidade_matriculas = sum(
            1 for m in self._matriculas
            if m.get_oferta() is oferta
        )

        if quantidade_matriculas >= oferta.get_limite_vagas():
            raise ValueError("Não há vagas disponíveis nesta oferta.")

        nova_matricula = Matricula(aluno, oferta)

        self._matriculas.append(nova_matricula)

        return nova_matricula

    def buscar_matricula(self, matricula_aluno, codigo_oferta):

        for matricula in self._matriculas:

            aluno = matricula.get_aluno()
            oferta = matricula.get_oferta()

            if (
                aluno.get_matricula() == matricula_aluno
                and oferta.get_codigo() == codigo_oferta
            ):
                return matricula

        return None

    def listar_matriculas(self):
        return self._matriculas.copy()

    def listar_matriculas_oferta(self, codigo_oferta):

        oferta = self.buscar_oferta(codigo_oferta)

        if oferta is None:
            raise ValueError("Oferta não encontrada.")

        return [
            matricula for matricula in self._matriculas
            if matricula.get_oferta() is oferta
        ]

    
    def remover_matricula(self, matricula_aluno, codigo_oferta):

        matricula = self.buscar_matricula(matricula_aluno, codigo_oferta)

        if matricula is None:
            raise ValueError("Matrícula não encontrada.")

        if matricula.listar_avaliacoes():
            raise ValueError(
                "Não é possível remover uma matrícula que possui avaliações registradas."
            )

        self._matriculas.remove(matricula)
        return matricula


    # ==================================
    # GERENCIAMENTO DE AVALIAÇÕES
    # ==================================

    def adicionar_avaliacao(self, matricula_aluno, codigo_oferta, descricao, nota):

        matricula = self.buscar_matricula(matricula_aluno, codigo_oferta)

        if matricula is None:
            raise ValueError("Matrícula não encontrada.")

        matricula.adicionar_avaliacao(descricao, nota)

    def remover_avaliacao(self, matricula_aluno, codigo_oferta, indice):

        matricula = self.buscar_matricula(matricula_aluno, codigo_oferta)

        if matricula is None:
            raise ValueError("Matrícula não encontrada.")

        matricula.remover_avaliacao(indice)


    def adicionar_avaliacao_professor(
        self, professor, matricula_aluno, codigo_oferta, descricao, nota
    ):

        oferta = self.buscar_oferta(codigo_oferta)

        if oferta is None:
            raise ValueError("Oferta não encontrada.")

        if oferta.get_professor() is not professor:
            raise ValueError("Você não tem autorização para alterar notas desta oferta.")

        self.adicionar_avaliacao(
            matricula_aluno, codigo_oferta, descricao, nota
        )


    def remover_avaliacao_professor(
        self, professor, matricula_aluno, codigo_oferta, indice
            ):

        oferta = self.buscar_oferta(codigo_oferta)

        if oferta is None:
            raise ValueError("Oferta não encontrada.")

        if oferta.get_professor() is not professor:
            raise ValueError("Você não tem autorização para alterar notas desta oferta.")

        self.remover_avaliacao(
            matricula_aluno, codigo_oferta, indice
        )


    def listar_avaliacoes(self, matricula_aluno, codigo_oferta):

        matricula = self.buscar_matricula(matricula_aluno, codigo_oferta)

        if matricula is None:
            raise ValueError("Matrícula não encontrada.")

        return matricula.listar_avaliacoes()

    def consultar_media(self, matricula_aluno, codigo_oferta):

        matricula = self.buscar_matricula(matricula_aluno, codigo_oferta)

        if matricula is None:
            raise ValueError("Matrícula não encontrada.")

        return matricula.calcular_media()

    def consultar_situacao(self, matricula_aluno, codigo_oferta):

        matricula = self.buscar_matricula(matricula_aluno, codigo_oferta)

        if matricula is None:
            raise ValueError("Matrícula não encontrada.")

        return matricula.verificar_situacao()

    # ==================================
    # CONSULTAS DE MATRÍCULAS
    # ==================================

    def listar_matriculas_aluno(self, matricula_aluno):

        aluno = self.buscar_aluno(matricula_aluno)

        if aluno is None:
            raise ValueError("Aluno não encontrado.")

        return [
            matricula for matricula in self._matriculas
            if matricula.get_aluno() is aluno
        ]

    def listar_matriculas_disciplina(self, codigo_disciplina):

        disciplina = self.buscar_disciplina(codigo_disciplina)

        if disciplina is None:
            raise ValueError("Disciplina não encontrada.")

        return [
            matricula for matricula in self._matriculas
            if matricula.get_oferta().get_disciplina() is disciplina
        ]

    def listar_disciplinas_aluno(self, matricula_aluno):

        matriculas = self.listar_matriculas_aluno(matricula_aluno)

        return [
            matricula.get_oferta().get_disciplina()
            for matricula in matriculas
        ]

    def listar_alunos_disciplina(self, codigo_disciplina):

        matriculas = self.listar_matriculas_disciplina(codigo_disciplina)

        return [
            matricula.get_aluno()
            for matricula in matriculas
        ]

        
