class Relatorio:
    def __init__(self, tipo_relatorio, dados_relatorio):
        self.tipo_relatorio = tipo_relatorio
        self.dados_relatorio = dados_relatorio

    def gerar_relatorio(self):
        linhas = [f"Relatorio: {self.tipo_relatorio}\n"]
        for item in self.dados_relatorio:
            linhas.append(str(item))
        return "\n".join(linhas)

    def salvar_em_arquivo(self, caminho_arquivo):
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            f.write(self.gerar_relatorio())