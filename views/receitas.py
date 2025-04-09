"""
Módulo de visualização da aba Receitas
"""
import tkinter as tk
from tkinter import ttk, messagebox
import datetime

class ReceitasFrame(ttk.Frame):
    """Frame para a aba de Receitas"""
    
    def __init__(self, parent, data_manager):
        """Inicializa o frame de Receitas"""
        super().__init__(parent)
        self.data_manager = data_manager
        
        # Configurando o layout
        self.configure(padding=20)
        
        # Criando os widgets
        self.criar_widgets()
        
        # Atualizando os dados
        self.atualizar()
    
    def criar_widgets(self):
        """Cria os widgets do frame"""
        # Frame para o título
        titulo_frame = ttk.Frame(self)
        titulo_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Título
        titulo_label = ttk.Label(
            titulo_frame, 
            text="Receitas", 
            style="Title.TLabel"
        )
        titulo_label.pack(side=tk.LEFT)
        
        # Botão para adicionar
        ttk.Button(
            titulo_frame, 
            text="Adicionar Receita", 
            command=self.abrir_formulario_adicionar
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
            command=self.atualizar
        ).pack(side=tk.LEFT)
        
        # Frame para a tabela
        tabela_frame = ttk.Frame(main_frame)
        tabela_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Criando a tabela (Treeview)
        colunas = ('descricao', 'valor', 'tipo', 'data')
        self.tabela = ttk.Treeview(
            tabela_frame, 
            columns=colunas, 
            show='headings',
            selectmode='browse'
        )
        
        # Configurando as colunas
        self.tabela.heading('descricao', text='Descrição')
        self.tabela.heading('valor', text='Valor (R$)')
        self.tabela.heading('tipo', text='Tipo')
        self.tabela.heading('data', text='Data')
        
        # Configurando a largura das colunas
        self.tabela.column('descricao', width=200)
        self.tabela.column('valor', width=100)
        self.tabela.column('tipo', width=100)
        self.tabela.column('data', width=150)
        
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
            command=self.editar_selecionado
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            botoes_frame,
            text="Excluir Selecionado",
            command=self.excluir_selecionado
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            botoes_frame,
            text="Atualizar Lista",
            command=self.atualizar
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
            
            # Obtendo as receitas do período selecionado
            receitas = self.data_manager.obter_receitas_por_periodo(mes, ano)
            
            # Adicionando as receitas à tabela
            for receita in receitas:
                # Formatando o valor
                valor = f"R$ {float(receita['valor']):.2f}"
                
                # Formatando o tipo
                tipo = "Recorrente" if receita.get('recorrente', False) else "Única"
                
                # Formatando a data
                data = receita.get('data', '')
                if not data and receita.get('recorrente', False):
                    data = f"Mensal desde {receita.get('data_inicio', '')}"
                    if 'data_fim' in receita and receita['data_fim']:
                        data += f" até {receita['data_fim']}"
                
                self.tabela.insert(
                    '', 
                    'end', 
                    values=(
                        receita['descricao'], 
                        valor,
                        tipo,
                        data
                    ),
                    tags=(str(receita['id']),)
                )
                
        except (ValueError, TypeError) as e:
            messagebox.showerror("Erro", f"Erro ao atualizar a tabela: {str(e)}")
    
    def obter_receita_selecionada(self):
        """Retorna o ID da receita selecionada ou None se nenhuma estiver selecionada"""
        selecao = self.tabela.selection()
        
        if not selecao:
            messagebox.showwarning("Aviso", "Nenhuma receita selecionada!")
            return None
        
        item = selecao[0]
        receita_id = int(self.tabela.item(item, 'tags')[0])
        
        return receita_id
    
    def editar_selecionado(self, event=None):
        """Edita a receita selecionada"""
        receita_id = self.obter_receita_selecionada()
        if receita_id:
            self.abrir_formulario_editar(receita_id)
    
    def excluir_selecionado(self):
        """Exclui a receita selecionada"""
        receita_id = self.obter_receita_selecionada()
        if receita_id:
            self.excluir_receita(receita_id)
    
    def abrir_menu_contexto(self, event):
        """Abre o menu de contexto ao clicar com o botão direito"""
        # Obtendo o item selecionado
        item = self.tabela.identify_row(event.y)
        
        if item:
            # Selecionando o item
            self.tabela.selection_set(item)
            
            # Obtendo o ID da receita
            receita_id = int(self.tabela.item(item, 'tags')[0])
            
            # Criando o menu de contexto
            menu = tk.Menu(self, tearoff=0)
            menu.add_command(label="Editar", command=lambda: self.abrir_formulario_editar(receita_id))
            menu.add_command(label="Excluir", command=lambda: self.excluir_receita(receita_id))
            
            # Exibindo o menu
            menu.post(event.x_root, event.y_root)
    
    def abrir_formulario_adicionar(self):
        """Abre o formulário para adicionar uma nova receita"""
        # Criando a janela do formulário
        formulario = tk.Toplevel(self)
        formulario.title("Adicionar Receita")
        formulario.geometry("500x400")
        formulario.resizable(False, False)
        
        # Criando o frame do formulário
        form_frame = ttk.Frame(formulario, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(
            form_frame, 
            text="Adicionar Receita", 
            style="Title.TLabel"
        ).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 20))
        
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
        
        # Tipo (Recorrente ou Única)
        ttk.Label(
            form_frame, 
            text="Tipo:"
        ).grid(row=row, column=0, sticky=tk.W, pady=5)
        
        tipo_frame = ttk.Frame(form_frame)
        tipo_frame.grid(row=row, column=1, sticky=tk.W, pady=5)
        
        recorrente_var = tk.BooleanVar(value=False)
        ttk.Radiobutton(
            tipo_frame, 
            text="Receita Única", 
            variable=recorrente_var, 
            value=False,
            command=lambda: self.atualizar_campos_tipo(data_frame, data_recorrente_frame, recorrente_var)
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Radiobutton(
            tipo_frame, 
            text="Receita Recorrente", 
            variable=recorrente_var, 
            value=True,
            command=lambda: self.atualizar_campos_tipo(data_frame, data_recorrente_frame, recorrente_var)
        ).pack(side=tk.LEFT)
        row += 1
        
        # Frame para data única
        data_frame = ttk.Frame(form_frame)
        data_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        ttk.Label(
            data_frame, 
            text="Data:"
        ).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        data_var = tk.StringVar(value=datetime.datetime.now().strftime("%d/%m/%Y"))
        ttk.Entry(
            data_frame, 
            textvariable=data_var, 
            width=10
        ).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Frame para data recorrente
        data_recorrente_frame = ttk.Frame(form_frame)
        data_recorrente_frame.grid(row=row+1, column=0, columnspan=2, sticky=tk.W, pady=5)
        data_recorrente_frame.grid_remove()  # Inicialmente oculto
        
        # Data de início
        ttk.Label(
            data_recorrente_frame, 
            text="Data de Início:"
        ).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        data_inicio_var = tk.StringVar(value=datetime.datetime.now().strftime("%d/%m/%Y"))
        ttk.Entry(
            data_recorrente_frame, 
            textvariable=data_inicio_var, 
            width=10
        ).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Data de fim (opcional)
        ttk.Label(
            data_recorrente_frame, 
            text="Data de Fim (opcional):"
        ).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        data_fim_var = tk.StringVar()
        ttk.Entry(
            data_recorrente_frame, 
            textvariable=data_fim_var, 
            width=10
        ).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        row += 2
        
        # Botões
        botoes_frame = ttk.Frame(form_frame)
        botoes_frame.grid(row=row, column=0, columnspan=2, sticky=tk.EW, pady=(20, 0))
        
        ttk.Button(
            botoes_frame, 
            text="Cancelar", 
            command=formulario.destroy
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            botoes_frame, 
            text="Salvar", 
            command=lambda: self.salvar_receita(
                formulario,
                descricao_var.get(),
                valor_var.get(),
                recorrente_var.get(),
                data_var.get() if not recorrente_var.get() else None,
                data_inicio_var.get() if recorrente_var.get() else None,
                data_fim_var.get() if recorrente_var.get() and data_fim_var.get() else None
            )
        ).pack(side=tk.RIGHT)
    
    def atualizar_campos_tipo(self, data_frame, data_recorrente_frame, recorrente_var):
        """Atualiza a visibilidade dos campos de acordo com o tipo de receita"""
        if recorrente_var.get():
            # Receita recorrente
            data_frame.grid_remove()
            data_recorrente_frame.grid()
        else:
            # Receita única
            data_frame.grid()
            data_recorrente_frame.grid_remove()
    
    def salvar_receita(self, formulario, descricao, valor, recorrente, data, data_inicio, data_fim):
        """Salva uma nova receita"""
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
        
        # Criando o dicionário da receita
        receita = {
            'descricao': descricao,
            'valor': valor,
            'recorrente': recorrente
        }
        
        # Adicionando campos específicos de acordo com o tipo de receita
        if recorrente:
            # Validando a data de início
            try:
                datetime.datetime.strptime(data_inicio, "%d/%m/%Y")
                receita['data_inicio'] = data_inicio
            except ValueError:
                messagebox.showerror("Erro", "A data de início deve estar no formato DD/MM/AAAA!")
                return
            
            # Adicionando a data de fim (se existir)
            if data_fim:
                try:
                    datetime.datetime.strptime(data_fim, "%d/%m/%Y")
                    receita['data_fim'] = data_fim
                except ValueError:
                    messagebox.showerror("Erro", "A data de fim deve estar no formato DD/MM/AAAA!")
                    return
        else:
            # Validando a data
            try:
                datetime.datetime.strptime(data, "%d/%m/%Y")
                receita['data'] = data
            except ValueError:
                messagebox.showerror("Erro", "A data deve estar no formato DD/MM/AAAA!")
                return
        
        # Adicionando a receita
        self.data_manager.adicionar_receita(receita)
        
        # Fechando o formulário
        formulario.destroy()
        
        # Atualizando a tabela
        self.atualizar()
    
    def abrir_formulario_editar(self, receita_id):
        """Abre o formulário para editar uma receita existente"""
        # Obtendo a receita
        receitas = self.data_manager.obter_receitas()
        receita = None
        
        for r in receitas:
            if r['id'] == receita_id:
                receita = r
                break
        
        if not receita:
            messagebox.showerror("Erro", "Receita não encontrada!")
            return
        
        # Criando a janela do formulário
        formulario = tk.Toplevel(self)
        formulario.title("Editar Receita")
        formulario.geometry("500x400")
        formulario.resizable(False, False)
        
        # Criando o frame do formulário
        form_frame = ttk.Frame(formulario, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(
            form_frame, 
            text="Editar Receita", 
            style="Title.TLabel"
        ).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 20))
        
        # Campos do formulário
        row = 1
        
        # Descrição
        ttk.Label(
            form_frame, 
            text="Descrição:"
        ).grid(row=row, column=0, sticky=tk.W, pady=5)
        
        descricao_var = tk.StringVar(value=receita['descricao'])
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
        
        valor_var = tk.StringVar(value=str(receita['valor']))
        ttk.Entry(
            form_frame, 
            textvariable=valor_var, 
            width=10
        ).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        # Tipo (Recorrente ou Única)
        ttk.Label(
            form_frame, 
            text="Tipo:"
        ).grid(row=row, column=0, sticky=tk.W, pady=5)
        
        tipo_frame = ttk.Frame(form_frame)
        tipo_frame.grid(row=row, column=1, sticky=tk.W, pady=5)
        
        recorrente_var = tk.BooleanVar(value=receita.get('recorrente', False))
        ttk.Radiobutton(
            tipo_frame, 
            text="Receita Única", 
            variable=recorrente_var, 
            value=False,
            command=lambda: self.atualizar_campos_tipo(data_frame, data_recorrente_frame, recorrente_var)
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Radiobutton(
            tipo_frame, 
            text="Receita Recorrente", 
            variable=recorrente_var, 
            value=True,
            command=lambda: self.atualizar_campos_tipo(data_frame, data_recorrente_frame, recorrente_var)
        ).pack(side=tk.LEFT)
        row += 1
        
        # Frame para data única
        data_frame = ttk.Frame(form_frame)
        data_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        ttk.Label(
            data_frame, 
            text="Data:"
        ).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        data_var = tk.StringVar(value=receita.get('data', datetime.datetime.now().strftime("%d/%m/%Y")))
        ttk.Entry(
            data_frame, 
            textvariable=data_var, 
            width=10
        ).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Frame para data recorrente
        data_recorrente_frame = ttk.Frame(form_frame)
        data_recorrente_frame.grid(row=row+1, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Data de início
        ttk.Label(
            data_recorrente_frame, 
            text="Data de Início:"
        ).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        data_inicio_var = tk.StringVar(value=receita.get('data_inicio', datetime.datetime.now().strftime("%d/%m/%Y")))
        ttk.Entry(
            data_recorrente_frame, 
            textvariable=data_inicio_var, 
            width=10
        ).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Data de fim (opcional)
        ttk.Label(
            data_recorrente_frame, 
            text="Data de Fim (opcional):"
        ).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        data_fim_var = tk.StringVar(value=receita.get('data_fim', ''))
        ttk.Entry(
            data_recorrente_frame, 
            textvariable=data_fim_var, 
            width=10
        ).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Configurando a visibilidade inicial dos campos
        self.atualizar_campos_tipo(data_frame, data_recorrente_frame, recorrente_var)
        
        row += 2
        
        # Botões
        botoes_frame = ttk.Frame(form_frame)
        botoes_frame.grid(row=row, column=0, columnspan=2, sticky=tk.EW, pady=(20, 0))
        
        ttk.Button(
            botoes_frame, 
            text="Cancelar", 
            command=formulario.destroy
        ).pack(side=tk.RIGHT, padx=5)
        
        ttk.Button(
            botoes_frame, 
            text="Salvar", 
            command=lambda: self.atualizar_receita(
                formulario,
                receita_id,
                descricao_var.get(),
                valor_var.get(),
                recorrente_var.get(),
                data_var.get() if not recorrente_var.get() else None,
                data_inicio_var.get() if recorrente_var.get() else None,
                data_fim_var.get() if recorrente_var.get() and data_fim_var.get() else None
            )
        ).pack(side=tk.RIGHT)
    
    def atualizar_receita(self, formulario, receita_id, descricao, valor, recorrente, data, data_inicio, data_fim):
        """Atualiza uma receita existente"""
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
        
        # Criando o dicionário da receita
        receita = {
            'id': receita_id,
            'descricao': descricao,
            'valor': valor,
            'recorrente': recorrente
        }
        
        # Adicionando campos específicos de acordo com o tipo de receita
        if recorrente:
            # Validando a data de início
            try:
                datetime.datetime.strptime(data_inicio, "%d/%m/%Y")
                receita['data_inicio'] = data_inicio
            except ValueError:
                messagebox.showerror("Erro", "A data de início deve estar no formato DD/MM/AAAA!")
                return
            
            # Adicionando a data de fim (se existir)
            if data_fim:
                try:
                    datetime.datetime.strptime(data_fim, "%d/%m/%Y")
                    receita['data_fim'] = data_fim
                except ValueError:
                    messagebox.showerror("Erro", "A data de fim deve estar no formato DD/MM/AAAA!")
                    return
        else:
            # Validando a data
            try:
                datetime.datetime.strptime(data, "%d/%m/%Y")
                receita['data'] = data
            except ValueError:
                messagebox.showerror("Erro", "A data deve estar no formato DD/MM/AAAA!")
                return
        
        # Atualizando a receita
        self.data_manager.atualizar_receita(receita_id, receita)
        
        # Fechando o formulário
        formulario.destroy()
        
        # Atualizando a tabela
        self.atualizar()
    
    def excluir_receita(self, receita_id):
        """Exclui uma receita"""
        # Confirmando a exclusão
        if messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir esta receita?"):
            # Excluindo a receita
            self.data_manager.excluir_receita(receita_id)
            
            # Atualizando a tabela
            self.atualizar()