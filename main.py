
import customtkinter as ctk

from services.gerenciamento import GerenciamentoAcademico
from services.autenticacao import AutenticacaoProfessor
from services.gerenciamento_professores import GerenciamentoProfessores
from views.tela_principal import TelaPrincipal


def main():

    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    gerenciamento = GerenciamentoAcademico()
    autenticacao = AutenticacaoProfessor()

    gerenciamento_professores = GerenciamentoProfessores(
        gerenciamento,
        autenticacao
    )

    app = TelaPrincipal(gerenciamento, gerenciamento_professores)
    app.mainloop()


if __name__ == "__main__":
    main()
