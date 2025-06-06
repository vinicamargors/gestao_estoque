from db import conectar_banco

def atualizar_tabela_vendas():
    conn = conectar_banco()
    cursor = conn.cursor()

    try:
        # Verifica se a coluna já existe
        cursor.execute("PRAGMA table_info(vendas)")
        colunas = [col[1] for col in cursor.fetchall()]
        if 'preco_base' not in colunas:
            cursor.execute("ALTER TABLE vendas ADD COLUMN preco_base REAL")
            print("✅ Coluna 'preco_base' adicionada com sucesso à tabela 'vendas'.")
        else:
            print("ℹ️ A coluna 'preco_base' já existe na tabela 'vendas'. Nenhuma alteração foi feita.")
        
        conn.commit()
    except Exception as e:
        print(f"❌ Erro ao atualizar a tabela: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    atualizar_tabela_vendas()
