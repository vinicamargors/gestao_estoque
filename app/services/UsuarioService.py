from app.repositories.interfaces.IUsuarioRepository import IUsuarioRepository
from app.models.Usuario import Usuario

class UsuarioService:
    def __init__(self, repo: IUsuarioRepository):
        self.repo = repo

    def criar_usuario(self, id, nome, email, senha, cargo, permissoes):
        usuario = Usuario(id, nome, email, senha, cargo, permissoes)
        self.repo.adicionar(usuario)

    def autenticar_usuario(self, email, senha):
        usuario = self.repo.buscar_por_email(email)
        if usuario and usuario.senha == senha:
            return usuario
        return None

    def listar_usuarios(self):
        return self.repo.listar_todos()
