"""
Módulo de visualização da aba Gastos Gerais com interface tradicional
"""
import tkinter as tk
from tkinter import ttk, messagebox
import datetime

class GastosGeraisFrame(ttk.Frame):
    """Frame para a aba de Gastos Gerais"""
    
    def __init__(self, parent, data_manager):
        """Inicializa o frame de Gastos Gerais"""
        super().__init__(parent)
        self.data_manager = data_manager
        
        # Configurando o layout
        self.configure(padding=10)
        
        # Criando os widgets
        self.criar_widgets()
        
        # Atualizando os dados
        self.atualizar()
    
    def criar_widgets(self):
        """Cria os widgets do frame"""
        # Frame para o título e botão adicionar
        titulo_frame = ttk.Frame(self)
        titulo_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Título
        titulo_label = ttk.Label(
            titulo_frame, 
            text="Gastos Gerais", 
            style="Title.TLabel"
        )
        titulo_label.pack(side=tk.LEFT)
        
        # Botão para adicionar
        ttk.Button(
            titulo_frame, 
            text="Adicionar Gasto",
            command=self.abrir_formulario_adicionar,
            width=15
        ).pack(side=tk.RIGHT)
        
        # Frame para a tabela e botões
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame para seleção de período
        periodo_frame = ttk.Frame(main_frame)
        periodo_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Obtendo o mês e ano atuais
        hoje = datetime.datetime.now()
        
        # Variáveis para o mês e ano selecionados
        self.filtro_mes_var = tk.StringVar(value=str(hoje.month))
        self.filtro_ano_var = tk.StringVar(value=str(hoje.year))
        
        # Label para o mês
        ttk.Label(periodo_frame, text="Mês:").pack(side=tk.LEFT, padx=(0, 5))
        
        # Combobox para o mês
        meses = [str(i) for i in range(1, 13)]
        mes_combo = ttk.Combobox(
            periodo_frame, 
            textvariable=self.filtro_mes_var, 
            values=meses, 
            width=3,
            state="readonly"
        )
        mes_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        # Label para o ano
        ttk.Label(periodo_frame, text="Ano:").pack(side=tk.LEFT, padx=(0, 5))
        
        # Combobox para o ano
        anos = [str(i) for i in range(hoje.year - 5, hoje.year + 6)]
        ano_combo = ttk.Combobox(
            periodo_frame, 
            textvariable=self.filtro_ano_var, 
            values=anos, 
            width=5,
            state="readonly"
        )
        ano_combo.pack(side=tk.LEFT, padx=(0, 10))
        
        # Botão para filtrar
        ttk.Button(
            periodo_frame, 
            text="Filtrar", 
            command=self.atualizar,
            width=10
        ).pack(side=tk.LEFT)
        
        # Frame para a tabela
        tabela_frame = ttk.Frame(main_frame, relief=tk.GROOVE, borderwidth=1)
        tabela_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Criando a tabela (Treeview)
        colunas = ('descricao', 'valor', 'categoria', 'data')
        self.tabela = ttk.Treeview(
            tabela_frame, 
            columns=colunas, 
            show='headings',
            selectmode='browse',
            style="Treeview"
        )
        
        # Configurando as colunas
        self.tabela.heading('descricao', text='Descrição')
        self.tabela.heading('valor', text='Valor (R$)')
        self.tabela.heading('categoria', text='Categoria')
        self.tabela.heading('data', text='Data')
        
        # Configurando a largura das colunas
        self.tabela.column('descricao', width=250)
        self.tabela.column('valor', width=120)
        self.tabela.column('categoria', width=150)
        self.tabela.column('data', width=120)
        
        # Adicionando a tabela ao frame com scrollbar
        self.tabela.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tabela_frame, orient=tk.VERTICAL, command=self.tabela.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tabela.configure(yscrollcommand=scrollbar.set)
        
        # Adicionando evento de clique duplo para editar
        self.tabela.bind("<Double-1>", self.editar_selecionado)
        
        # Mantendo o menu de contexto como opção adicional
        self.tabela.bind("<Button-3>", self.abrir_menu_contexto)
        
        # Frame para os botões de ação
        botoes_frame = ttk.Frame(main_frame)
        botoes_frame.pack(fill=tk.X, pady=(5, 0))
        
        # Botões de ação
        ttk.Button(
            botoes_frame,
            text="Editar Selecionado",
            command=self.editar_selecionado,
            width=15
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            botoes_frame,
            text="Excluir Selecionado",
            command=self.excluir_selecionado,
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            botoes_frame,
            text="Atualizar Lista",
            command=self.atualizar,
            width=15
        ).pack(side=tk.RIGHT)
    
    def atualizar(self, event=None):
        """Atualiza os dados da tabela"""
        # Limpando a tabela
        for item in self.tabela.get_children():
            self.tabela.delete(item)
        
        try:
            # Obtendo o mês e ano selecionados
            mes = int(self.filtro_mes_var.get())
            ano = int(self.filtro_ano_var.get())
            
            # Obtendo os gastos do período selecionado
            gastos = self.data_manager.obter_gastos_por_periodo(mes, ano)
            
            # Adicionando os gastos à tabela
            for gasto in gastos:
                # Formatando o valor
                valor = f"R$ {float(gasto['valor']):.2f}"
                
                # Formatando a categoria
                categoria = gasto.get('categoria', 'Sem categoria')
                
                # Formatando a data
                data = gasto.get('data', '')
                
                self.tabela.insert(
                    '', 
                    'end', 
                    values=(
                        gasto['descricao'], 
                        valor,
                        categoria,
                        data
                    ),
                    tags=(str(gasto['id']),)
                )
                
        except (ValueError, TypeError) as e:
            messagebox.showerror("Erro", f"Erro ao atualizar a tabela: {str(e)}")
    
    def obter_gasto_selecionado(self):
        """Retorna o ID do gasto selecionado ou None se nenhum estiver selecionado"""
        selecao = self.tabela.selection()
        
        if not selecao:
            messagebox.showwarning("Aviso", "Nenhum gasto selecionado!")
            return None
        
        item = selecao[0]
        gasto_id = int(self.tabela.item(item, 'tags')[0])
        
        return gasto_id
    
    def editar_selecionado(self, event=None):
        """Edita o gasto selecionado"""
        gasto_id = self.obter_gasto_selecionado()
        if gasto_id:
            self.abrir_formulario_editar(gasto_id)
    
    def excluir_selecionado(self):
        """Exclui o gasto selecionado"""
        gasto_id = self.obter_gasto_selecionado()
        if gasto_id:
            self.excluir_gasto(gasto_id)
    
    def abrir_menu_contexto(self, event):
        """Abre o menu de contexto ao clicar com o botão direito"""
        # Obtendo o item selecionado
        item = self.tabela.identify_row(event.y)
        
        if item:
            # Selecionando o item
            self.tabela.selection_set(item)
            
            # Obtendo o ID do gasto
            gasto_id = int(self.tabela.item(item, 'tags')[0])
            
            # Criando o menu de contexto
            menu = tk.Menu(self, tearoff=0)
            menu.add_command(label="Editar", command=lambda: self.abrir_formulario_editar(gasto_id))
            menu.add_command(label="Excluir", command=lambda: self.excluir_gasto(gasto_id))
            
            # Exibindo o menu
            menu.post(event.x_root, event.y_root)
    
    def abrir_formulario_adicionar(self):
        """Abre o formulário para adicionar um novo gasto"""
        # Criando a janela do formulário
        formulario = tk.Toplevel(self)
        formulario.title("Adicionar Gasto")
        formulario.geometry("400x300")
        formulario.resizable(False, False)
        formulario.transient(self.winfo_toplevel())
        formulario.grab_set()
        
        # Criando o frame do formulário
        form_frame = ttk.Frame(formulario, padding=15)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(
            form_frame, 
            text="Adicionar Gasto", 
            style="Title.TLabel"
        ).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 15))
        
        # Campos do formulário
        row = 1
        
        # Descrição
        ttk.Label(
            form_frame, 
            text="Descrição:"
        ).grid(row=row, column=0, sticky=tk.W, pady=5)
        
        descricao_var = tk.StringVar()
        ttk.Entry(
            form_frame, 
            textvariable=descricao_var, 
            width=30
        ).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        # Valor
        ttk.Label(
            form_frame, 
            text="Valor (R$):"
        ).grid(row=row, column=0, sticky=tk.W, pady=5)
        
        valor_var = tk.StringVar()
        ttk.Entry(
            form_frame, 
            textvariable=valor_var, 
            width=10
        ).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        # Categoria
        ttk.Label(
            form_frame, 
            text="Categoria:"
        ).grid(row=row, column=0, sticky=tk.W, pady=5)
        
        # Obtendo as categorias existentes
        categorias = self.data_manager.obter_categorias_gastos()
        
        categoria_var = tk.StringVar()
        ttk.Combobox(
            form_frame, 
            textvariable=categoria_var, 
            values=categorias, 
            width=20
        ).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        # Data
        ttk.Label(
            form_frame, 
            text="Data:"
        ).grid(row=row, column=0, sticky=tk.W, pady=5)
        
        data_var = tk.StringVar(value=datetime.datetime.now().strftime("%d/%m/%Y"))
        ttk.Entry(
            form_frame, 
            textvariable=data_var, 
            width=10
        ).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        # Botões
        botoes_frame = ttk.Frame(form_frame)
        botoes_frame.grid(row=row, column=0, columnspan=2, sticky=tk.EW, pady=(15, 0))
        
        ttk.Button(
            botoes_frame, 
            text="Cancelar", 
            command=formulario.destroy,
            width=10
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            botoes_frame, 
            text="Salvar", 
            width=10,
            command=lambda: self.salvar_gasto(
                formulario,
                descricao_var.get(),
                valor_var.get(),
                categoria_var.get(),
                data_var.get()
            )
        ).pack(side=tk.RIGHT)
    
    def salvar_gasto(self, formulario, descricao, valor, categoria, data):
        """Salva um novo gasto"""
        # Validando os campos
        if not descricao:
            messagebox.showerror("Erro", "A descrição é obrigatória!")
            return
        
        try:
            valor = float(valor.replace(',', '.'))
            if valor <= 0:
                raise ValueError("O valor deve ser maior que zero!")
        except ValueError:
            messagebox.showerror("Erro", "O valor deve ser um número válido maior que zero!")
            return
        
        # Validando a data
        try:
            datetime.datetime.strptime(data, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Erro", "A data deve estar no formato DD/MM/AAAA!")
            return
        
        # Criando o dicionário do gasto
        gasto = {
            'descricao': descricao,
            'valor': valor,
            'categoria': categoria,
            'data': data
        }
        
        # Adicionando o gasto
        self.data_manager.adicionar_gasto(gasto)
        
        # Fechando o formulário
        formulario.destroy()
        
        # Atualizando a tabela
        self.atualizar()
    
    def abrir_formulario_editar(self, gasto_id):
        """Abre o formulário para editar um gasto existente"""
        # Obtendo o gasto
        gastos = self.data_manager.obter_gastos()
        gasto = None
        
        for g in gastos:
            if g['id'] == gasto_id:
                gasto = g
                break
        
        if not gasto:
            messagebox.showerror("Erro", "Gasto não encontrado!")
            return
        
        # Criando a janela do formulário
        formulario = tk.Toplevel(self)
        formulario.title("Editar Gasto")
        formulario.geometry("400x300")
        formulario.resizable(False, False)
        formulario.transient(self.winfo_toplevel())
        formulario.grab_set()
        
        # Criando o frame do formulário
        form_frame = ttk.Frame(formulario, padding=15)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(
            form_frame, 
            text="Editar Gasto", 
            style="Title.TLabel"
        ).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 15))
        
        # Campos do formulário
        row = 1
        
        # Descrição
        ttk.Label(
            form_frame, 
            text="Descrição:"
        ).grid(row=row, column=0, sticky=tk.W, pady=5)
        
        descricao_var = tk.StringVar(value=gasto['descricao'])
        ttk.Entry(
            form_frame, 
            textvariable=descricao_var, 
            width=30
        ).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        # Valor
        ttk.Label(
            form_frame, 
            text="Valor (R$):"
        ).grid(row=row, column=0, sticky=tk.W, pady=5)
        
        valor_var = tk.StringVar(value=str(gasto['valor']))
        ttk.Entry(
            form_frame, 
            textvariable=valor_var, 
            width=10
        ).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        # Categoria
        ttk.Label(
            form_frame, 
            text="Categoria:"
        ).grid(row=row, column=0, sticky=tk.W, pady=5)
        
        # Obtendo as categorias existentes
        categorias = self.data_manager.obter_categorias_gastos()
        
        categoria_var = tk.StringVar(value=gasto.get('categoria', ''))
        ttk.Combobox(
            form_frame, 
            textvariable=categoria_var, 
            values=categorias, 
            width=20
        ).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        # Data
        ttk.Label(
            form_frame, 
            text="Data:"
        ).grid(row=row, column=0, sticky=tk.W, pady=5)
        
        data_var = tk.StringVar(value=gasto.get('data', datetime.datetime.now().strftime("%d/%m/%Y")))
        ttk.Entry(
            form_frame, 
            textvariable=data_var, 
            width=10
        ).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        # Botões
        botoes_frame = ttk.Frame(form_frame)
        botoes_frame.grid(row=row, column=0, columnspan=2, sticky=tk.EW, pady=(15, 0))
        
        ttk.Button(
            botoes_frame, 
            text="Cancelar", 
            command=formulario.destroy,
            width=10
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            botoes_frame, 
            text="Salvar", 
            width=10,
            command=lambda: self.atualizar_gasto(
                formulario,
                gasto_id,
                descricao_var.get(),
                valor_var.get(),
                categoria_var.get(),
                data_var.get()
            )
        ).pack(side=tk.RIGHT)
    
    def atualizar_gasto(self, formulario, gasto_id, descricao, valor, categoria, data):
        """Atualiza um gasto existente"""
        # Validando os campos
        if not descricao:
            messagebox.showerror("Erro", "A descrição é obrigatória!")
            return
        
        try:
            valor = float(valor.replace(',', '.'))
            if valor <= 0:
                raise ValueError("O valor deve ser maior que zero!")
        except ValueError:
            messagebox.showerror("Erro", "O valor deve ser um número válido maior que zero!")
            return
        
        # Validando a data
        try:
            datetime.datetime.strptime(data, "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Erro", "A data deve estar no formato DD/MM/AAAA!")
            return
        
        # Criando o dicionário do gasto
        gasto = {
            'id': gasto_id,
            'descricao': descricao,
            'valor': valor,
            'categoria': categoria,
            'data': data
        }
        
        # Atualizando o gasto
        self.data_manager.atualizar_gasto(gasto_id, gasto)
        
        # Fechando o formulário
        formulario.destroy()
        
        # Atualizando a tabela
        self.atualizar()
    
    def excluir_gasto(self, gasto_id):
        """Exclui um gasto"""
        # Confirmando a exclusão
        if messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir este gasto?"):
            # Excluindo o gasto
            self.data_manager.excluir_gasto(gasto_id)
            
            # Atualizando a tabela
            self.atualizar()