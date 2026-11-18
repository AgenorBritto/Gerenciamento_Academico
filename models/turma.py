class Turma:

    def __init__(self, codigo, curso, periodo_ingresso, limite_alunos=40):
        self.set_codigo(codigo)
        self.set_curso(curso)
        self.set_periodo_ingresso(periodo_ingresso)
        self.set_limite_alunos(limite_alunos)

    def get_codigo(self):
        return self._codigo

    def set_codigo(self, codigo):

        if not isinstance(codigo, str):
            raise TypeError("O código deve ser um texto.")

        codigo = codigo.strip()

        if not codigo:
            raise ValueError("O código não pode ficar vazio.")

        self._codigo = codigo

    def get_curso(self):
        return self._curso

    def set_curso(self, curso):

        if not isinstance(curso, str):
            raise TypeError("O curso deve ser um texto.")

        curso = curso.strip()

        if not curso:
            raise ValueError("O curso não pode ficar vazio.")

        self._curso = curso

    def get_periodo_ingresso(self):
        return self._periodo_ingresso

    def set_periodo_ingresso(self, periodo_ingresso):

        if not isinstance(periodo_ingresso, str):
            raise TypeError("O período de ingresso deve ser um texto.")

        periodo_ingresso = periodo_ingresso.strip()

        if not periodo_ingresso:
            raise ValueError("O período de ingresso não pode ficar vazio.")

        self._periodo_ingresso = periodo_ingresso

    def get_limite_alunos(self):
        return self._limite_alunos

    def set_limite_alunos(self, limite_alunos):

        if isinstance(limite_alunos, bool) or not isinstance(limite_alunos, int):
            raise TypeError("O limite de alunos deve ser um número inteiro.")

        if limite_alunos <= 0:
            raise ValueError("O limite de alunos deve ser maior que zero.")

        self._limite_alunos = limite_alunos

    def apresentar(self):

        return (
            f"Turma: {self.get_codigo()} | "
            f"Curso: {self.get_curso()} | "
            f"Período: {self.get_periodo_ingresso()} | "
            f"Limite: {self.get_limite_alunos()} alunos"
        )
