import tkinter as tk
from tkinter import ttk, messagebox
from db import conectar_banco, criar_tabelas
from datetime import datetime, date
from logger import registrar_log

def abrir_menu_principal():
    janela = tk.Tk()
    janela.title("Sistema de Estoque - Menu Principal")
    janela.geometry("1100x550")

    # Frame de filtros
    frame_filtros = tk.Frame(janela)
    frame_filtros.pack(pady=10)

    tk.Label(frame_filtros, text="Filtrar por nome:").grid(row=0, column=0)
    entrada_nome = tk.Entry(frame_filtros)
    entrada_nome.grid(row=0, column=1, padx=5)

    tk.Label(frame_filtros, text="Filtrar por validade (AAAA-MM-DD):").grid(row=0, column=2)
    entrada_validade = tk.Entry(frame_filtros)
    entrada_validade.grid(row=0, column=3, padx=5)

    def aplicar_filtro():
        nome = entrada_nome.get()
        validade = entrada_validade.get()
        for item in tree.get_children():
            tree.delete(item)

        conn = conectar_banco()
        cursor = conn.cursor()
        query = "SELECT * FROM produtos WHERE 1=1"
        params = []

        if nome:
            query += " AND nome LIKE ?"
            params.append(f"%{nome}%")
        if validade:
            query += " AND data_validade = ?"
            params.append(validade)

        cursor.execute(query, params)
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)
        conn.close()
        registrar_log(f"Aplicou filtro - Nome: '{nome}', Validade: '{validade}'")

    def limpar_filtro():
        entrada_nome.delete(0, tk.END)
        entrada_validade.delete(0, tk.END)
        carregar_dados()
        registrar_log("Filtro limpo")

    tk.Button(frame_filtros, text="Buscar", command=aplicar_filtro).grid(row=0, column=4, padx=5)
    tk.Button(frame_filtros, text="Limpar", command=limpar_filtro).grid(row=0, column=5, padx=5)

    # Tabela
    colunas = ("ID", "Nome", "Categoria", "Fornecedor", "Entrada", "Validade", "Qtd", "Preço Base", "Preço Sugerido")
    tree = ttk.Treeview(janela, columns=colunas, show="headings")

    for col in colunas:
        tree.heading(col, text=col)
        tree.column(col, anchor=tk.CENTER, width=120)
    tree.pack(expand=True, fill=tk.BOTH)

    def carregar_dados():
        for item in tree.get_children():
            tree.delete(item)
        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produtos")
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)
        conn.close()
        registrar_log("Listou todos os produtos")

    def inserir_produto():
        form = tk.Toplevel(janela)
        form.title("Inserir Produto")

        campos = ["Nome", "Categoria", "Fornecedor", "Data Entrada", "Data Validade", "Quantidade", "Preço Base"]
        entradas = []

        for campo in campos:
            tk.Label(form, text=campo).pack()
            e = tk.Entry(form)
            e.pack()
            entradas.append(e)

        def salvar():
            dados = [e.get() for e in entradas]
            conn = conectar_banco()
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO produtos (nome, categoria, fornecedor, data_entrada, data_validade, quantidade, preco_base)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, dados)
            conn.commit()
            conn.close()
            registrar_log(f"Inseriu produto: {dados[0]} (Validade: {dados[4]})")
            messagebox.showinfo("Inserido", "Produto inserido com sucesso.")
            form.destroy()
            carregar_dados()

        tk.Button(form, text="Salvar", command=salvar).pack(pady=10)

    def editar_produto():
        item = tree.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um produto.")
            return

        dados = tree.item(item)['values']
        form = tk.Toplevel(janela)
        form.title("Editar Produto")

        campos = ["Nome", "Categoria", "Fornecedor", "Data Entrada", "Data Validade", "Quantidade", "Preço Base"]
        entradas = []

        for i, campo in enumerate(campos):
            tk.Label(form, text=campo).pack()
            e = tk.Entry(form)
            valor = dados[i + 1]
            if campo == "Preço Base":
                valor = str(valor).replace("R$", "").strip().replace(",", ".")
            e.insert(0, valor)
            e.pack()
            entradas.append(e)

        def salvar_edicao():
            novos_dados = [e.get() for e in entradas]
            conn = conectar_banco()
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE produtos
                SET nome=?, categoria=?, fornecedor=?, data_entrada=?, data_validade=?, quantidade=?, preco_base=?
                WHERE id=?
            """, (*novos_dados, dados[0]))
            conn.commit()
            conn.close()
            registrar_log(f"Editou produto ID {dados[0]} → Novo nome: {novos_dados[0]}, Validade: {novos_dados[4]}")
            messagebox.showinfo("Atualizado", "Produto atualizado com sucesso.")
            form.destroy()
            carregar_dados()

        tk.Button(form, text="Salvar Alterações", command=salvar_edicao).pack(pady=10)

    def vender_produto():
        item = tree.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um produto para vender.")
            return

        dados = tree.item(item)['values']
        produto_id = dados[0]
        categoria = dados[2]
        fornecedor = dados[3]
        data_entrada = dados[4]
        data_validade = dados[5]
        qtd_estoque = int(dados[6])
        preco_base = float(str(dados[7]).replace("R$", "").replace(",", "."))
        nome_exibicao = f"{categoria} - {fornecedor}"  # apenas para exibição no título

        validade_date = datetime.strptime(data_validade, "%Y-%m-%d").date()
        dias_restantes = (validade_date - date.today()).days

        if dias_restantes > 30:
            preco_sugerido = preco_base
        elif 15 < dias_restantes <= 30:
            preco_sugerido = preco_base * 0.9
        elif 10 < dias_restantes <= 15:
            preco_sugerido = preco_base * 0.7
        elif 5 < dias_restantes <= 10:
            preco_sugerido = preco_base * 0.5
        elif 2 < dias_restantes <= 5:
            preco_sugerido = preco_base * 0.25
        else:
            preco_sugerido = 0  # Produto vencido ou próximo de vencer

        preco_sugerido = round(preco_sugerido, 2)

        def confirmar_venda():
            try:
                qtd_venda = int(entry_qtd.get())
                if qtd_venda <= 0:
                    raise ValueError

                if qtd_venda > qtd_estoque:
                    messagebox.showerror("Erro", "Quantidade em estoque insuficiente.")
                    return

                nova_qtd = qtd_estoque - qtd_venda
                data_venda = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                conn = conectar_banco()
                cursor = conn.cursor()

                # Atualiza ou remove do estoque
                if nova_qtd == 0:
                    cursor.execute("DELETE FROM produtos WHERE id = ?", (produto_id,))
                    registrar_log(f"Venda de {qtd_venda} unidade(s) - Produto ID {produto_id} removido do estoque (zerado).")
                else:
                    cursor.execute("UPDATE produtos SET quantidade = ? WHERE id = ?", (nova_qtd, produto_id))
                    registrar_log(f"Venda de {qtd_venda} unidade(s) - Produto ID: {produto_id}, Restante: {nova_qtd}")

                # Registra a venda
                cursor.execute("""
                    INSERT INTO vendas (produto_id, data_venda, quantidade, preco_base, preco_venda)
                    VALUES (?, ?, ?, ?, ?)""",
                    (produto_id, data_venda, qtd_venda, preco_base, preco_sugerido))

                conn.commit()
                conn.close()

                messagebox.showinfo("Sucesso", f"{qtd_venda} unidade(s) vendidas por R$ {preco_sugerido:.2f} cada.")
                venda_janela.destroy()
                carregar_dados()

            except ValueError:
                messagebox.showerror("Erro", "Informe uma quantidade válida.")

        venda_janela = tk.Toplevel(janela)
        venda_janela.title(f"Vender - {nome_exibicao}")

        tk.Label(venda_janela, text=f"Quantidade disponível: {qtd_estoque}").pack(pady=5)
        tk.Label(venda_janela, text=f"Preço sugerido: R$ {preco_sugerido:.2f}").pack(pady=5)
        tk.Label(venda_janela, text="Quantidade a vender:").pack()
        entry_qtd = tk.Entry(venda_janela)
        entry_qtd.pack(pady=5)

        tk.Button(venda_janela, text="Confirmar Venda", command=confirmar_venda).pack(pady=10)

    def ver_historico_vendas():
        historico_janela = tk.Toplevel(janela)
        historico_janela.title("Histórico de Vendas")
        historico_janela.geometry("800x400")

        colunas = ("ID", "ID Produto", "Nome", "Quantidade", "Preço Base", "Preço Venda", "Data da Venda")
        tree_vendas = ttk.Treeview(historico_janela, columns=colunas, show="headings")

        for col in colunas:
            tree_vendas.heading(col, text=col)
            tree_vendas.column(col, anchor=tk.CENTER, width=120)
        tree_vendas.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT v.id, v.produto_id, p.nome, v.quantidade, v.preco_base, v.preco_venda, v.data_venda
            FROM vendas v
            JOIN produtos p ON v.produto_id = p.id
            ORDER BY v.data_venda DESC
        """)
        for row in cursor.fetchall():
            tree_vendas.insert("", tk.END, values=row)
        conn.close()


        conn.close()

        registrar_log("Visualizou histórico de vendas")

    def excluir_produto():
        item = tree.focus()
        if not item:
            messagebox.showwarning("Atenção", "Selecione um produto.")
            return
        dados = tree.item(item)['values']
        confirm = messagebox.askyesno("Confirmar", f"Deseja excluir o produto '{dados[1]}'?")
        if confirm:
            conn = conectar_banco()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM produtos WHERE id=?", (dados[0],))
            conn.commit()
            conn.close()
            registrar_log(f"Excluiu produto: ID {dados[0]} - {dados[1]}")
            carregar_dados()
            messagebox.showinfo("Excluído", "Produto excluído com sucesso.")

    def sugestao_venda():
        hoje = datetime.today().date()

        for item in tree.get_children():
            tree.delete(item)

        conn = conectar_banco()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produtos")
        produtos = cursor.fetchall()
        conn.close()

        alerta_ativos = []

        for prod in produtos:
            id, nome, cat, forn, entrada, validade, qtd, preco_base = prod
            preco_base = float(preco_base)
            validade_date = datetime.strptime(validade, "%Y-%m-%d").date()
            dias_restantes = (validade_date - hoje).days

            if dias_restantes > 30:
                preco_sugerido = preco_base
            elif 15 < dias_restantes <= 30:
                preco_sugerido = preco_base * 0.9
            elif 10 < dias_restantes <= 15:
                preco_sugerido = preco_base * 0.7
            elif 5 < dias_restantes <= 10:
                preco_sugerido = preco_base * 0.5
            elif 2 < dias_restantes <= 5:
                preco_sugerido = preco_base * 0.25
            else:
                preco_sugerido = 0
                alerta_ativos.append(
                    f"⚠ PRODUTO: [{id} - {nome.upper()}]\nVENCE HOJE OU ESTÁ VENCIDO → RETIRE DA PRATELEIRA\n"
                )

            preco_sugerido = round(preco_sugerido, 2)

            tree.insert("", tk.END, values=(
                id, nome, cat, forn, entrada, validade, qtd,
                f"R$ {preco_base:.2f}",
                f"R$ {preco_sugerido:.2f}" if preco_sugerido > 0 else "RETIRE"
            ))

        if alerta_ativos:
            messagebox.showwarning("Alerta de Vencimento", "\n".join(alerta_ativos))
        else:
            messagebox.showinfo("Sugestão", "Produtos sugeridos com base na validade.")
        registrar_log("Consultou sugestão de venda baseada na validade dos produtos")

        def voltar_visualizacao():
            for item in tree.get_children():
                tree.delete(item)
            carregar_dados()
            btn_voltar.destroy()
            registrar_log("Retornou à visualização padrão dos produtos")

        btn_voltar = tk.Button(janela, text="← Voltar", command=voltar_visualizacao, bg="#e0e0e0")
        btn_voltar.pack(pady=5)

    # Botões
    frame_botoes = tk.Frame(janela)
    frame_botoes.pack(pady=10)

    tk.Button(frame_botoes, text="Inserir", command=inserir_produto).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botoes, text="Editar", command=editar_produto).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botoes, text="Excluir", command=excluir_produto).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botoes, text="Ver Sugestão de Venda", command=sugestao_venda).pack(side=tk.LEFT, padx=5)
    tk.Button(frame_botoes, text="Histórico de Vendas", command=ver_historico_vendas).pack(side=tk.LEFT, padx=5)
    tk.Button(janela, text="Vender", command=vender_produto).pack(pady=10)

    carregar_dados()
    janela.mainloop()
