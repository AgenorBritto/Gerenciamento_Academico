class Disciplina:
    def __init__(self, codigo, nome):
        self.set_codigo(codigo)
        self.set_nome(nome)

    def get_codigo(self):
        return self._codigo

    def set_codigo(self, codigo):
        if not isinstance(codigo, str):
            raise TypeError("O código deve ser um texto.")
        codigo = codigo.strip()
        if not codigo:
            raise ValueError("O código não pode ficar vazio.")
        self._codigo = codigo

    def get_nome(self):
        return self._nome

    def set_nome(self, nome):
        if not isinstance(nome, str):
            raise TypeError("O nome deve ser um texto.")
        nome = nome.strip()
        if not nome:
            raise ValueError("O nome da disciplina não pode ficar vazio.")
        self._nome = nome

    def apresentar(self):
        return f"Disciplina: {self.get_nome()} | Código: {self.get_codigo()}"
