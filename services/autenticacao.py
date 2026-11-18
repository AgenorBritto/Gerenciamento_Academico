
import hashlib
import hmac
import secrets


class AutenticacaoProfessor:

    def __init__(self):
        self._acessos = {}

    def _validar_texto(self, valor, campo):
        if not isinstance(valor, str):
            raise TypeError(f"{campo} deve ser um texto.")

        valor = valor.strip()

        if not valor:
            raise ValueError(f"{campo} não pode ficar vazio.")

        return valor

    def _validar_senha(self, senha):
        if not isinstance(senha, str):
            raise TypeError("A senha deve ser um texto.")

        if not senha.strip():
            raise ValueError("A senha não pode ficar vazia.")

        if len(senha) < 6:
            raise ValueError("A senha deve possuir pelo menos 6 caracteres.")

        return senha

    def _gerar_hash(self, senha, salt):
        return hashlib.pbkdf2_hmac(
            "sha256",
            senha.encode("utf-8"),
            salt,
            100000
        )

    def _usuario_existe(self, usuario, codigo_ignorado=None):
        for codigo, dados in self._acessos.items():
            if codigo != codigo_ignorado and dados["usuario"].casefold() == usuario.casefold():
                return True

        return False

    def cadastrar_acesso(self, codigo, usuario, senha):
        codigo = self._validar_texto(codigo, "O código do professor")
        usuario = self._validar_texto(usuario, "O usuário")
        senha = self._validar_senha(senha)

        if codigo in self._acessos:
            raise ValueError("Este professor já possui um acesso cadastrado.")

        if self._usuario_existe(usuario):
            raise ValueError("Este nome de usuário já está em uso.")

        salt = secrets.token_bytes(16)
        senha_hash = self._gerar_hash(senha, salt)

        self._acessos[codigo] = {
            "usuario": usuario,
            "salt": salt,
            "senha_hash": senha_hash
        }

    def editar_acesso(self, codigo, novo_usuario, nova_senha="", novo_codigo=None):
        codigo = self._validar_texto(codigo, "O código do professor")
        novo_usuario = self._validar_texto(novo_usuario, "O usuário")

        if codigo not in self._acessos:
            raise ValueError("Acesso do professor não encontrado.")

        codigo_destino = codigo if novo_codigo is None else self._validar_texto(novo_codigo, "O novo código")

        if codigo_destino != codigo and codigo_destino in self._acessos:
            raise ValueError("Já existe um acesso associado a esse código.")

        if self._usuario_existe(novo_usuario, codigo):
            raise ValueError("Este nome de usuário já está em uso.")

        if not isinstance(nova_senha, str):
            raise TypeError("A senha deve ser um texto.")

        dados = self._acessos[codigo]

        if nova_senha:
            nova_senha = self._validar_senha(nova_senha)
            salt = secrets.token_bytes(16)
            senha_hash = self._gerar_hash(nova_senha, salt)
        else:
            salt = dados["salt"]
            senha_hash = dados["senha_hash"]

        novos_dados = {
            "usuario": novo_usuario,
            "salt": salt,
            "senha_hash": senha_hash
        }

        del self._acessos[codigo]
        self._acessos[codigo_destino] = novos_dados

    def excluir_acesso(self, codigo):
        codigo = self._validar_texto(codigo, "O código do professor")

        if codigo not in self._acessos:
            raise ValueError("Acesso do professor não encontrado.")

        del self._acessos[codigo]

    def obter_usuario(self, codigo):
        codigo = self._validar_texto(codigo, "O código do professor")

        dados = self._acessos.get(codigo)

        if dados is None:
            return None

        return dados["usuario"]

    def validar_login(self, usuario, senha):
        if not isinstance(usuario, str) or not isinstance(senha, str):
            return None

        usuario = usuario.strip()

        if not usuario or not senha:
            return None

        for codigo, dados in self._acessos.items():
            if dados["usuario"].casefold() == usuario.casefold():
                senha_hash = self._gerar_hash(senha, dados["salt"])

                if hmac.compare_digest(senha_hash, dados["senha_hash"]):
                    return codigo

                return None

        return None
