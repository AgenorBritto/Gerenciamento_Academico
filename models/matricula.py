from models.aluno import Aluno
from models.oferta_disciplina import OfertaDisciplina


class Matricula:
    def __init__(self, aluno, oferta):
        if not isinstance(aluno, Aluno):
            raise TypeError("É necessário informar um objeto Aluno.")

        if not isinstance(oferta, OfertaDisciplina):
            raise TypeError("É necessário informar um objeto OfertaDisciplina.")

        self._aluno = aluno
        self._oferta = oferta
        self._avaliacoes = []

    def get_aluno(self):
        return self._aluno

    def get_oferta(self):
        return self._oferta

    def adicionar_avaliacao(self, descricao, nota):
        if not isinstance(descricao, str):
            raise TypeError("A descrição da avaliação deve ser um texto.")

        descricao = descricao.strip()

        if not descricao:
            raise ValueError("A descrição da avaliação não pode ficar vazia.")

        if isinstance(nota, bool) or not isinstance(nota, (int, float)):
            raise TypeError("A nota deve ser um número.")

        if nota < 0 or nota > 10:
            raise ValueError("A nota deve estar entre 0 e 10.")

        self._avaliacoes.append({"descricao": descricao, "nota": float(nota)})

    def remover_avaliacao(self, indice):
        if isinstance(indice, bool) or not isinstance(indice, int):
            raise TypeError("O índice deve ser um número inteiro.")

        if indice < 0 or indice >= len(self._avaliacoes):
            raise ValueError("Avaliação não encontrada.")

        self._avaliacoes.pop(indice)

    def listar_avaliacoes(self):
        return [avaliacao.copy() for avaliacao in self._avaliacoes]

    def calcular_media(self):
        if not self._avaliacoes:
            return 0

        notas = [avaliacao["nota"] for avaliacao in self._avaliacoes]
        return sum(notas) / len(notas)

    def verificar_situacao(self):
        if not self._avaliacoes:
            return "Sem notas"

        media = self.calcular_media()

        if media >= 7:
            return "Aprovado"

        return "Reprovado"
