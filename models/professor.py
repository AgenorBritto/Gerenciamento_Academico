
from models.pessoa import Pessoa


class Professor(Pessoa):

    def __init__(self, nome, idade, codigo, especialidade):
        super().__init__(nome, idade)

        self.set_codigo(codigo)
        self.set_especialidade(especialidade)

    # Getter e Setter do código
    def get_codigo(self):
        return self._codigo

    def set_codigo(self, codigo):
        if not isinstance(codigo, str):
            raise TypeError("O código deve ser um texto.")

        codigo = codigo.strip()

        if not codigo:
            raise ValueError("O código não pode ficar vazio.")

        self._codigo = codigo

    # Getter e Setter da especialidade
    def get_especialidade(self):
        return self._especialidade

    def set_especialidade(self, especialidade):
        if not isinstance(especialidade, str):
            raise TypeError("A especialidade deve ser um texto.")

        especialidade = especialidade.strip()

        if not especialidade:
            raise ValueError("A especialidade não pode ficar vazia.")

        self._especialidade = especialidade

    # Implementação do método abstrato
    def apresentar(self):
        return (
            f"Professor: {self.get_nome()} | "
            f"Código: {self.get_codigo()} | "
            f"Especialidade: {self.get_especialidade()}"
        )
