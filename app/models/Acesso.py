class Acesso:
    def __init__(self, usuario):
        self.usuario = usuario

    def possui_permissao(self, permissao):
        return self.usuario.verificar_permissao(permissao)

    def login(self, email, senha):
        return self.usuario.email == email and self.usuario.senha == senha
