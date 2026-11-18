from models.disciplina import Disciplina
from models.professor import Professor


class OfertaDisciplina:
    def __init__(self, codigo, disciplina, professor, codigo_turma, periodo, limite_vagas=40):
        self.set_codigo(codigo)
        self.set_disciplina(disciplina)
        self.set_professor(professor)
        self.set_codigo_turma(codigo_turma)
        self.set_periodo(periodo)
        self.set_limite_vagas(limite_vagas)

    def get_codigo(self):
        return self._codigo

    def set_codigo(self, codigo):
        if not isinstance(codigo, str):
            raise TypeError("O código da oferta deve ser um texto.")
        codigo = codigo.strip()
        if not codigo:
            raise ValueError("O código da oferta não pode ficar vazio.")
        self._codigo = codigo

    def get_disciplina(self):
        return self._disciplina

    def set_disciplina(self, disciplina):
        if not isinstance(disciplina, Disciplina):
            raise TypeError("É necessário informar um objeto Disciplina.")
        self._disciplina = disciplina

    def get_professor(self):
        return self._professor

    def set_professor(self, professor):
        if not isinstance(professor, Professor):
            raise TypeError("É necessário informar um objeto Professor.")
        self._professor = professor

    def get_codigo_turma(self):
        return self._codigo_turma

    def set_codigo_turma(self, codigo_turma):
        if not isinstance(codigo_turma, str):
            raise TypeError("O código da turma deve ser um texto.")
        codigo_turma = codigo_turma.strip()
        if not codigo_turma:
            raise ValueError("O código da turma não pode ficar vazio.")
        self._codigo_turma = codigo_turma

    def get_periodo(self):
        return self._periodo

    def set_periodo(self, periodo):
        if not isinstance(periodo, str):
            raise TypeError("O período deve ser um texto.")
        periodo = periodo.strip()
        if not periodo:
            raise ValueError("O período não pode ficar vazio.")
        self._periodo = periodo

    def get_limite_vagas(self):
        return self._limite_vagas

    def set_limite_vagas(self, limite_vagas):
        if isinstance(limite_vagas, bool) or not isinstance(limite_vagas, int):
            raise TypeError("O limite de vagas deve ser um número inteiro.")
        if limite_vagas <= 0:
            raise ValueError("O limite de vagas deve ser maior que zero.")
        self._limite_vagas = limite_vagas

    def apresentar(self):
        return (
            f"Oferta: {self.get_codigo()} | "
            f"Disciplina: {self.get_disciplina().get_nome()} | "
            f"Professor: {self.get_professor().get_nome()} | "
            f"Turma: {self.get_codigo_turma()} | "
            f"Período: {self.get_periodo()} | "
            f"Vagas: {self.get_limite_vagas()}"
        )
