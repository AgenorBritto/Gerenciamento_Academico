
from abc import ABC, abstractmethod


class Pessoa(ABC):

    def __init__(self, nome, idade):
        self.set_nome(nome)
        self.set_idade(idade)

    def get_nome(self):
        return self._nome

    def set_nome(self, nome):
        if not isinstance(nome, str):
            raise TypeError("O nome deve ser um texto.")

        nome = nome.strip()

        if not nome:
            raise ValueError("O nome não pode ficar vazio.")

        self._nome = nome

    def get_idade(self):
        return self._idade

    def set_idade(self, idade):
        if isinstance(idade, bool) or not isinstance(idade, int):
            raise TypeError("A idade deve ser um número inteiro.")

        if idade <= 0:
            raise ValueError("A idade deve ser maior que zero.")

        self._idade = idade

    @abstractmethod
    def apresentar(self):
        pass
