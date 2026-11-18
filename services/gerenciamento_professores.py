
class GerenciamentoProfessores:

    def __init__(self, gerenciamento, autenticacao):
        self.gerenciamento = gerenciamento
        self.autenticacao = autenticacao

    def cadastrar_professor(self, professor, usuario, senha):
        codigo = professor.get_codigo()

        self.gerenciamento.cadastrar_professor(professor)

        try:
            self.autenticacao.cadastrar_acesso(codigo, usuario, senha)

        except (ValueError, TypeError):
            self.gerenciamento.excluir_professor(codigo)
            raise

        return professor

    def editar_professor(
        self,
        codigo_atual,
        novo_nome=None,
        nova_idade=None,
        novo_codigo=None,
        nova_especialidade=None,
        novo_usuario=None,
        nova_senha=""
    ):

        professor = self.gerenciamento.buscar_professor(codigo_atual)

        if professor is None:
            raise ValueError("Professor não encontrado.")

        usuario_atual = self.autenticacao.obter_usuario(codigo_atual)

        if usuario_atual is None:
            raise ValueError("Professor não possui acesso cadastrado.")

        usuario = usuario_atual if novo_usuario is None else novo_usuario

        codigo = professor.get_codigo() if novo_codigo is None else novo_codigo

        dados_originais = {
            "nome": professor.get_nome(),
            "idade": professor.get_idade(),
            "codigo": professor.get_codigo(),
            "especialidade": professor.get_especialidade()
        }

        professor_atualizado = self.gerenciamento.editar_professor(
            codigo_atual,
            novo_nome=novo_nome,
            nova_idade=nova_idade,
            novo_codigo=novo_codigo,
            nova_especialidade=nova_especialidade
        )

        try:
            self.autenticacao.editar_acesso(
                codigo_atual,
                usuario,
                nova_senha,
                codigo
            )

        except (ValueError, TypeError):
            self.gerenciamento.editar_professor(
                codigo,
                novo_nome=dados_originais["nome"],
                nova_idade=dados_originais["idade"],
                novo_codigo=dados_originais["codigo"],
                nova_especialidade=dados_originais["especialidade"]
            )
            raise

        return professor_atualizado

    def excluir_professor(self, codigo):
        usuario = self.autenticacao.obter_usuario(codigo)

        if usuario is None:
            raise ValueError("Professor não possui acesso cadastrado.")

        professor = self.gerenciamento.excluir_professor(codigo)
        self.autenticacao.excluir_acesso(codigo)

        return professor

    def autenticar_professor(self, usuario, senha):
        codigo = self.autenticacao.validar_login(usuario, senha)

        if codigo is None:
            return None

        return self.gerenciamento.buscar_professor(codigo)

    def obter_usuario(self, codigo):
        return self.autenticacao.obter_usuario(codigo)