class Usuario:
    def __init__(self, id, nome, email, senha, cargo, permissoes=None):
        self.id = id
        self.nome = nome
        self.email = email
        self.senha = senha  # Em produção, deve ser criptografada
        self.cargo = cargo
        self.permissoes = permissoes or []

    def verificar_permissao(self, permissao):
        return permissao in self.permissoes

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "cargo": self.cargo,
            "permissoes": self.permissoes
        }