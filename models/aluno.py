from models.pessoa import Pessoa
from models.turma import Turma


class Aluno(Pessoa):

    def __init__(self, nome, idade, matricula, turma):
        super().__init__(nome, idade)
        self.set_matricula(matricula)
        self.set_turma(turma)

    def get_matricula(self):
        return self._matricula

    def set_matricula(self, matricula):

        if not isinstance(matricula, str):
            raise TypeError("A matrícula deve ser um texto.")

        matricula = matricula.strip()

        if not matricula:
            raise ValueError("A matrícula não pode ficar vazia.")

        self._matricula = matricula

    def get_turma(self):
        return self._turma

    def set_turma(self, turma):

        if not isinstance(turma, Turma):
            raise TypeError("É necessário informar um objeto Turma.")

        self._turma = turma

    def apresentar(self):

        return (
            f"Aluno: {self.get_nome()} | "
            f"Matrícula: {self.get_matricula()} | "
            f"Turma: {self.get_turma().get_codigo()}"
        )
