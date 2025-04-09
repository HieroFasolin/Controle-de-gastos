"""
Módulo de visualização da aba Contas Fixas
"""
import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import calendar

class ContasFixasFrame(ttk.Frame):
    """Frame para a aba de Contas Fixas"""

    def __init__(self, parent, data_manager):
        """Inicializa o frame de Contas Fixas"""
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
            text="Contas Fixas", 
            style="Title.TLabel"
        )
        titulo_label.pack(side=tk.LEFT)
        
        # Botão para adicionar
        ttk.Button(
            titulo_frame, 
            text="Adicionar Conta Fixa", 
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
        colunas = ('descricao', 'valor', 'periodo', 'status', 'parcelas', 'data_limite')
        self.tabela = ttk.Treeview(
            tabela_frame, 
            columns=colunas, 
            show='headings',
            selectmode='browse'
        )
        
        # Configurando as colunas
        self.tabela.heading('descricao', text='Descrição')
        self.tabela.heading('valor', text='Valor (R$)')
        self.tabela.heading('periodo', text='Período')
        self.tabela.heading('status', text='Status')
        self.tabela.heading('parcelas', text='Parcelas')
        self.tabela.heading('data_limite', text='Data Limite')
        
        # Configurando a largura das colunas
        self.tabela.column('descricao', width=200)
        self.tabela.column('valor', width=100)
        self.tabela.column('periodo', width=200)
        self.tabela.column('status', width=100)
        self.tabela.column('parcelas', width=100)
        self.tabela.column('data_limite', width=100)
        
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
        
        # Novo botão para marcar como pago
        ttk.Button(
            botoes_frame,
            text="Marcar como Pago",
            command=self.marcar_como_pago
        ).pack(side=tk.LEFT, padx=5)
        
        # Novo botão para marcar como pendente
        ttk.Button(
            botoes_frame,
            text="Marcar como Pendente",
            command=self.marcar_como_pendente
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
            
            # Obtendo as contas fixas
            contas_fixas = self.data_manager.obter_contas_fixas()
            
            # Filtrando as contas fixas pelo período selecionado
            contas_filtradas = []
            for conta in contas_fixas:
                # Para contas recorrentes
                if conta.get('recorrente', False):
                    # Verificando se a data de início é anterior ou igual ao período selecionado
                    data_inicio = conta.get('data_inicio', '')
                    if data_inicio:
                        try:
                            data_inicio_obj = datetime.datetime.strptime(data_inicio, "%d/%m/%Y")
                            data_periodo = datetime.datetime(ano, mes, 1)
                            
                            # Verificando se a data de fim é posterior ou igual ao período selecionado
                            data_fim = conta.get('data_fim', '')
                            if data_fim:
                                data_fim_obj = datetime.datetime.strptime(data_fim, "%d/%m/%Y")
                                if data_inicio_obj <= data_periodo and data_fim_obj >= data_periodo:
                                    contas_filtradas.append(conta)
                            else:
                                # Se não tiver data de fim, considera que a conta ainda está ativa
                                if data_inicio_obj <= data_periodo:
                                    contas_filtradas.append(conta)
                        except ValueError:
                            # Se houver erro na conversão da data, inclui a conta
                            contas_filtradas.append(conta)
                # Para contas não recorrentes
                else:
                    # Verificando se o mês e ano correspondem ao período selecionado
                    if conta.get('mes') == mes and conta.get('ano') == ano:
                        contas_filtradas.append(conta)
            
            # Adicionando as contas fixas à tabela
            for conta in contas_filtradas:
                # Formatando o valor
                valor = f"R$ {float(conta['valor']):.2f}"
                
                # Formatando o período
                if conta.get('recorrente', False):
                    data_inicio = conta['data_inicio']
                    
                    if 'data_fim' in conta and conta['data_fim']:
                        data_fim = conta['data_fim']
                        periodo = f"{data_inicio} até {data_fim}"
                    else:
                        periodo = f"{data_inicio} em diante"
                else:
                    mes = conta['mes']
                    ano = conta['ano']
                    periodo = f"{mes:02d}/{ano}"
                
                # Verificando se a conta está paga para o período selecionado
                pago = self.data_manager.verificar_conta_paga(conta['id'], mes, ano)
                
                # Formatando o status
                status = "Pago" if pago else "Pendente"
                
                # Verificando se é uma conta parcelada
                parcelas_info = ""
                if conta.get('parcelado', False):
                    num_parcelas = conta.get('num_parcelas', 1)
                    valor_original = float(conta['valor'])
                    valor_parcela = valor_original / num_parcelas
                    
                    # Formatando a informação de parcelas com o valor de cada parcela
                    parcelas_info = f"{num_parcelas}x de R$ {valor_parcela:.2f}"
                    
                    # Verificando se tem juros
                    if 'valor_com_juros' in conta and conta['valor_com_juros']:
                        valor_com_juros = float(conta['valor_com_juros'])
                        valor_sem_juros = float(conta['valor'])
                        
                        # Calculando o valor dos juros
                        juros = valor_com_juros - valor_sem_juros
                        
                        # Calculando o valor da parcela com juros
                        valor_parcela_com_juros = valor_com_juros / num_parcelas
                        
                        # Atualizando a informação de parcelas com o valor com juros
                        parcelas_info = f"{num_parcelas}x de R$ {valor_parcela_com_juros:.2f}"
                        
                        # Adicionando informação de juros ao valor
                        valor = f"R$ {valor_sem_juros:.2f} + {juros:.2f} (juros)"
                
                # Obtendo a data limite de pagamento
                data_limite = conta.get('data_limite', '-')
                
                # Adicionando à tabela
                self.tabela.insert(
                    '', 
                    'end', 
                    values=(
                        conta['descricao'],
                        valor,
                        periodo,
                        status,
                        parcelas_info,
                        data_limite
                    ),
                    tags=(conta['id'],)
                )
                
                # Adicionando cor de fundo para contas pagas
                if pago:
                    item_id = self.tabela.get_children()[-1]
                    self.tabela.item(item_id, tags=(conta['id'], 'pago'))
                    self.tabela.tag_configure('pago', background='#e6ffe6')  # Verde claro
        except (ValueError, TypeError) as e:
            messagebox.showerror("Erro", f"Erro ao atualizar a tabela: {str(e)}")

    def obter_conta_selecionada(self):
        """Retorna o ID da conta selecionada ou None se nenhuma estiver selecionada"""
        selecao = self.tabela.selection()
        
        if not selecao:
            messagebox.showwarning("Aviso", "Nenhuma conta selecionada!")
            return None
        
        item = selecao[0]
        conta_id = int(self.tabela.item(item, 'tags')[0])
        
        return conta_id

    def editar_selecionado(self, event=None):
        """Edita a conta selecionada"""
        conta_id = self.obter_conta_selecionada()
        if conta_id:
            self.abrir_formulario_editar(conta_id)

    def excluir_selecionado(self):
        """Exclui a conta selecionada"""
        conta_id = self.obter_conta_selecionada()
        if conta_id:
            self.excluir_conta(conta_id)
    
    def marcar_como_pago(self):
        """Marca a conta selecionada como paga para o período atual"""
        conta_id = self.obter_conta_selecionada()
        if conta_id:
            try:
                # Obtendo o mês e ano selecionados
                mes = int(self.filtro_mes_var.get())
                ano = int(self.filtro_ano_var.get())
                
                # Marcando a conta como paga
                self.data_manager.marcar_conta_como_paga(conta_id, mes, ano)
                
                # Atualizando a tabela
                self.atualizar()
                
                messagebox.showinfo("Sucesso", "Conta marcada como paga!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao marcar conta como paga: {str(e)}")
    
    def marcar_como_pendente(self):
        """Marca a conta selecionada como pendente para o período atual"""
        conta_id = self.obter_conta_selecionada()
        if conta_id:
            try:
                # Obtendo o mês e ano selecionados
                mes = int(self.filtro_mes_var.get())
                ano = int(self.filtro_ano_var.get())
                
                # Marcando a conta como pendente
                self.data_manager.marcar_conta_como_paga(conta_id, mes, ano, status_pago=False)
                
                # Atualizando a tabela
                self.atualizar()
                
                messagebox.showinfo("Sucesso", "Conta marcada como pendente!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao marcar conta como pendente: {str(e)}")

    def abrir_menu_contexto(self, event):
        """Abre o menu de contexto ao clicar com o botão direito"""
        # Obtendo o item selecionado
        item = self.tabela.identify_row(event.y)
        
        if item:
            # Selecionando o item
            self.tabela.selection_set(item)
            
            # Obtendo o ID da conta
            conta_id = int(self.tabela.item(item, 'tags')[0])
            
            # Obtendo o mês e ano selecionados
            mes = int(self.filtro_mes_var.get())
            ano = int(self.filtro_ano_var.get())
            
            # Verificando se a conta está paga
            pago = self.data_manager.verificar_conta_paga(conta_id, mes, ano)
            
            # Criando o menu de contexto
            menu = tk.Menu(self, tearoff=0)
            menu.add_command(label="Editar", command=lambda: self.abrir_formulario_editar(conta_id))
            menu.add_command(label="Excluir", command=lambda: self.excluir_conta(conta_id))
            menu.add_separator()
            
            # Adicionando opções para marcar como pago/pendente
            if pago:
                menu.add_command(label="Marcar como Pendente", 
                                command=lambda: self.marcar_como_pendente_menu(conta_id, mes, ano))
            else:
                menu.add_command(label="Marcar como Pago", 
                                command=lambda: self.marcar_como_pago_menu(conta_id, mes, ano))
            
            # Exibindo o menu
            menu.post(event.x_root, event.y_root)
    
    def marcar_como_pago_menu(self, conta_id, mes, ano):
        """Marca a conta como paga a partir do menu de contexto"""
        try:
            # Marcando a conta como paga
            self.data_manager.marcar_conta_como_paga(conta_id, mes, ano)
            
            # Atualizando a tabela
            self.atualizar()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao marcar conta como paga: {str(e)}")
    
    def marcar_como_pendente_menu(self, conta_id, mes, ano):
        """Marca a conta como pendente a partir do menu de contexto"""
        try:
            # Marcando a conta como pendente
            self.data_manager.marcar_conta_como_paga(conta_id, mes, ano, status_pago=False)
            
            # Atualizando a tabela
            self.atualizar()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao marcar conta como pendente: {str(e)}")

    def abrir_formulario_adicionar(self):
        """Abre o formulário para adicionar uma nova conta fixa"""
        # Criando a janela do formulário
        formulario = tk.Toplevel(self)
        formulario.title("Adicionar Conta Fixa")
        formulario.geometry("500x650")
        formulario.resizable(False, False)
        
        # Criando o frame do formulário
        form_frame = ttk.Frame(formulario, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(
            form_frame, 
            text="Adicionar Conta Fixa", 
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
        
        # Checkbox para conta recorrente
        recorrente_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            form_frame, 
            text="Conta Recorrente", 
            variable=recorrente_var,
            command=lambda: self.atualizar_campos_recorrente(form_frame, recorrente_var, data_inicio_frame, data_fim_frame, mes_ano_frame)
        ).grid(row=row, column=0, sticky=tk.W, pady=5)
        row += 1
        
        # Frame para data de início (inicialmente oculto)
        data_inicio_frame = ttk.Frame(form_frame)
        data_inicio_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        data_inicio_frame.grid_remove()  # Inicialmente oculto
        
        ttk.Label(
            data_inicio_frame, 
            text="Data de Início:"
        ).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        data_inicio_var = tk.StringVar(value=datetime.datetime.now().strftime("%d/%m/%Y"))
        ttk.Entry(
            data_inicio_frame, 
            textvariable=data_inicio_var, 
            width=10
        ).grid(row=0, column=1, sticky=tk.W, pady=5)
        row += 1
        
        # Frame para data de fim (inicialmente oculto)
        data_fim_frame = ttk.Frame(form_frame)
        data_fim_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        data_fim_frame.grid_remove()  # Inicialmente oculto
        
        ttk.Label(
            data_fim_frame, 
            text="Data de Fim (opcional):"
        ).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        data_fim_var = tk.StringVar()
        ttk.Entry(
            data_fim_frame, 
            textvariable=data_fim_var, 
            width=10
        ).grid(row=0, column=1, sticky=tk.W, pady=5)
        row += 1
        
        # Frame para mês e ano (inicialmente visível)
        mes_ano_frame = ttk.Frame(form_frame)
        mes_ano_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Mês
        ttk.Label(
            mes_ano_frame, 
            text="Mês:"
        ).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        mes_var = tk.StringVar(value=str(datetime.datetime.now().month))
        meses = [str(i) for i in range(1, 13)]
        ttk.Combobox(
            mes_ano_frame, 
            textvariable=mes_var, 
            values=meses, 
            width=3,
            state="readonly"
        ).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Ano
        ttk.Label(
            mes_ano_frame, 
            text="Ano:"
        ).grid(row=0, column=2, sticky=tk.W, pady=5, padx=(10, 0))
        
        ano_atual = datetime.datetime.now().year
        ano_var = tk.StringVar(value=str(ano_atual))
        anos = [str(i) for i in range(ano_atual - 5, ano_atual + 6)]
        ttk.Combobox(
            mes_ano_frame, 
            textvariable=ano_var, 
            values=anos, 
            width=5,
            state="readonly"
        ).grid(row=0, column=3, sticky=tk.W, pady=5)
        row += 1
        
        # Novo campo: Data limite de pagamento
        ttk.Label(
            form_frame, 
            text="Dia de Vencimento:"
        ).grid(row=row, column=0, sticky=tk.W, pady=5)

        data_limite_var = tk.StringVar()
        ttk.Entry(
            form_frame, 
            textvariable=data_limite_var, 
            width=10
        ).grid(row=row, column=1, sticky=tk.W, pady=5)

        # Adicionando um botão de ajuda para explicar o campo
        ttk.Button(
            form_frame,
            text="?",
            width=2,
            command=lambda: messagebox.showinfo(
                "Ajuda", 
                "Informe o dia do mês em que esta conta vence (1-31).\n"
                "Você também pode informar uma data completa no formato DD/MM/AAAA.\n"
                "O sistema irá lembrá-lo quando a data estiver próxima."
            )
        ).grid(row=row, column=1, sticky=tk.E, pady=5)
        row += 1
        
        # Variável para controlar se a conta é parcelada
        parcelado_var = tk.BooleanVar(value=False)
        
        # Checkbox para marcar como parcelada
        ttk.Checkbutton(
            form_frame,
            text="Conta Parcelada",
            variable=parcelado_var,
            command=lambda: self.atualizar_campos_parcelamento(form_frame, parcelado_var, parcelamento_frame, data_fim_frame, recorrente_var)
        ).grid(row=row, column=0, sticky=tk.W, pady=5)
        row += 1
        
        # Frame para opções de parcelamento (inicialmente oculto)
        parcelamento_frame = ttk.Frame(form_frame)
        parcelamento_frame.grid(row=row, column=0, columnspan=2, sticky=tk.EW, pady=5)
        parcelamento_frame.grid_remove()  # Inicialmente oculto
        row += 1
        
        # Número de parcelas
        ttk.Label(
            parcelamento_frame,
            text="Número de Parcelas:"
        ).grid(row=0, column=0, sticky=tk.W, pady=2)
        
        num_parcelas_var = tk.StringVar(value="1")
        ttk.Spinbox(
            parcelamento_frame,
            from_=1,
            to=99,
            textvariable=num_parcelas_var,
            width=5
        ).grid(row=0, column=1, sticky=tk.W, pady=2)
        
        # Opção de juros
        tem_juros_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            parcelamento_frame,
            text="Incluir Juros",
            variable=tem_juros_var,
            command=lambda: self.atualizar_campos_juros(parcelamento_frame, tem_juros_var, juros_frame, valor_var, valor_com_juros_var)
        ).grid(row=1, column=0, sticky=tk.W, pady=2)
        
        # Frame para opções de juros (inicialmente oculto)
        juros_frame = ttk.Frame(parcelamento_frame)
        juros_frame.grid(row=2, column=0, columnspan=2, sticky=tk.EW, pady=2)
        juros_frame.grid_remove()  # Inicialmente oculto
        
        # Valor total com juros
        ttk.Label(
            juros_frame,
            text="Valor Total com Juros (R$):"
        ).grid(row=0, column=0, sticky=tk.W, pady=2)
        
        valor_com_juros_var = tk.StringVar(value="0.00")
        ttk.Entry(
            juros_frame,
            textvariable=valor_com_juros_var,
            width=10
        ).grid(row=0, column=1, sticky=tk.W, pady=2)
        
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
            command=lambda: self.salvar_conta(
                formulario,
                descricao_var.get(),
                valor_var.get(),
                recorrente_var.get(),
                data_inicio_var.get() if recorrente_var.get() else None,
                data_fim_var.get() if recorrente_var.get() and data_fim_var.get() else None,
                int(mes_var.get()) if not recorrente_var.get() else None,
                int(ano_var.get()) if not recorrente_var.get() else None,
                parcelado_var.get(),
                int(num_parcelas_var.get()) if parcelado_var.get() else None,
                tem_juros_var.get() if parcelado_var.get() else False,
                valor_com_juros_var.get() if parcelado_var.get() and tem_juros_var.get() else None,
                data_limite_var.get()  # Novo parâmetro
            )
        ).pack(side=tk.RIGHT)

    def atualizar_campos_recorrente(self, form_frame, recorrente_var, data_inicio_frame, data_fim_frame, mes_ano_frame):
        """Atualiza a visibilidade dos campos de acordo com a opção de recorrência"""
        if recorrente_var.get():
            # Se for recorrente, mostra os campos de data de início e fim
            data_inicio_frame.grid()
            data_fim_frame.grid()
            mes_ano_frame.grid_remove()
        else:
            # Se não for recorrente, mostra os campos de mês e ano
            data_inicio_frame.grid_remove()
            data_fim_frame.grid_remove()
            mes_ano_frame.grid()

    def atualizar_campos_parcelamento(self, form_frame, parcelado_var, parcelamento_frame, data_fim_frame, recorrente_var):
        """Atualiza a visibilidade dos campos de parcelamento"""
        if parcelado_var.get():
            parcelamento_frame.grid()
            
            # Se for parcelado, oculta o campo de data de fim
            if recorrente_var.get():
                data_fim_frame.grid_remove()
        else:
            parcelamento_frame.grid_remove()
            
            # Se não for parcelado, mostra o campo de data de fim
            if recorrente_var.get():
                data_fim_frame.grid()

    def atualizar_campos_juros(self, parcelamento_frame, tem_juros_var, juros_frame, valor_var, valor_com_juros_var):
        """Atualiza a visibilidade dos campos de juros"""
        if tem_juros_var.get():
            juros_frame.grid()
            
            # Pré-preenche o valor com juros com o valor atual
            try:
                valor_atual = float(valor_var.get())
                valor_com_juros_var.set(f"{valor_atual:.2f}")
            except ValueError:
                pass
        else:
            juros_frame.grid_remove()

    def salvar_conta(self, formulario, descricao, valor, recorrente, data_inicio, data_fim, mes, ano, parcelado, num_parcelas, tem_juros, valor_com_juros, data_limite):
        """Salva uma nova conta fixa"""
        # Validando os campos
        if not descricao:
            messagebox.showerror("Erro", "A descrição é obrigatória!")
            return
        
        try:
            valor = float(valor)
            if valor <= 0:
                raise ValueError("O valor deve ser maior que zero!")
        except ValueError:
            messagebox.showerror("Erro", "O valor deve ser um número válido maior que zero!")
            return
        
        # Criando o dicionário da conta
        conta = {
            'descricao': descricao,
            'valor': valor,
            'recorrente': recorrente
        }
        
        # Adicionando campos específicos de acordo com o tipo de conta
        if recorrente:
            # Validando a data de início
            try:
                datetime.datetime.strptime(data_inicio, "%d/%m/%Y")
                conta['data_inicio'] = data_inicio
            except ValueError:
                messagebox.showerror("Erro", "A data de início deve estar no formato DD/MM/AAAA!")
                return
            
            # Adicionando a data de fim (se existir)
            if data_fim:
                try:
                    datetime.datetime.strptime(data_fim, "%d/%m/%Y")
                    conta['data_fim'] = data_fim
                except ValueError:
                    messagebox.showerror("Erro", "A data de fim deve estar no formato DD/MM/AAAA!")
                    return
        else:
            # Adicionando o mês e ano
            conta['mes'] = mes
            conta['ano'] = ano
        
        # Adicionando a data limite de pagamento (se existir)
        if data_limite:
            try:
                # Verificando se é apenas um número (dia)
                if data_limite.isdigit() and 1 <= int(data_limite) <= 31:
                    # Armazenando apenas o dia
                    conta['data_limite'] = data_limite
                else:
                    # Tentando interpretar como uma data completa
                    datetime.datetime.strptime(data_limite, "%d/%m/%Y")
                    conta['data_limite'] = data_limite
            except ValueError:
                messagebox.showerror("Erro", "A data limite deve ser um dia do mês (1-31) ou uma data completa no formato DD/MM/AAAA!")
                return
        
        # Adicionando informações de parcelamento
        if parcelado:
            conta['parcelado'] = True
            conta['num_parcelas'] = num_parcelas
            
            # Adicionando informações de juros
            if tem_juros:
                try:
                    valor_com_juros = float(valor_com_juros)
                    if valor_com_juros <= valor:
                        messagebox.showerror("Erro", "O valor com juros deve ser maior que o valor original!")
                        return
                    conta['valor_com_juros'] = valor_com_juros
                except ValueError:
                    messagebox.showerror("Erro", "O valor com juros deve ser um número válido!")
                    return
            
            # Calculando automaticamente a data de fim se for uma conta recorrente parcelada
            if recorrente and not data_fim:
                try:
                    # Convertendo a data de início para um objeto datetime
                    data_inicio_obj = datetime.datetime.strptime(data_inicio, "%d/%m/%Y")
                    
                    # Calculando a data de fim (data de início + número de parcelas meses)
                    data_fim_obj = data_inicio_obj
                    for _ in range(num_parcelas - 1):  # -1 porque a primeira parcela é na data de início
                        # Avançando um mês
                        mes = data_fim_obj.month + 1
                        ano = data_fim_obj.year
                        if mes > 12:
                            mes = 1
                            ano += 1
                        
                        # Ajustando o dia para o último dia do mês se necessário
                        ultimo_dia = calendar.monthrange(ano, mes)[1]
                        dia = min(data_fim_obj.day, ultimo_dia)
                        
                        # Criando a nova data
                        data_fim_obj = datetime.datetime(ano, mes, dia)
                    
                    # Formatando a data de fim
                    conta['data_fim'] = data_fim_obj.strftime("%d/%m/%Y")
                    
                except Exception as e:
                    # Se ocorrer algum erro, apenas não define a data de fim
                    pass
        
        # Adicionando a conta
        self.data_manager.adicionar_conta_fixa(conta)
        
        # Fechando o formulário
        formulario.destroy()
        
        # Atualizando a tabela
        self.atualizar()

    def abrir_formulario_editar(self, conta_id):
        """Abre o formulário para editar uma conta fixa existente"""
        # Obtendo a conta
        contas = self.data_manager.obter_contas_fixas()
        conta = None
        
        for c in contas:
            if c['id'] == conta_id:
                conta = c
                break
        
        if not conta:
            messagebox.showerror("Erro", "Conta não encontrada!")
            return
        
        # Criando a janela do formulário
        formulario = tk.Toplevel(self)
        formulario.title("Editar Conta Fixa")
        formulario.geometry("500x650")
        formulario.resizable(False, False)
        
        # Criando o frame do formulário
        form_frame = ttk.Frame(formulario, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(
            form_frame, 
            text="Editar Conta Fixa", 
            style="Title.TLabel"
        ).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 20))
        
        # Campos do formulário
        row = 1
        
        # Descrição
        ttk.Label(
            form_frame, 
            text="Descrição:"
        ).grid(row=row, column=0, sticky=tk.W, pady=5)
        
        descricao_var = tk.StringVar(value=conta['descricao'])
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
        
        valor_var = tk.StringVar(value=str(conta['valor']))
        ttk.Entry(
            form_frame, 
            textvariable=valor_var, 
            width=10
        ).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        # Checkbox para conta recorrente
        recorrente_var = tk.BooleanVar(value=conta.get('recorrente', False))
        ttk.Checkbutton(
            form_frame, 
            text="Conta Recorrente", 
            variable=recorrente_var,
            command=lambda: self.atualizar_campos_recorrente(form_frame, recorrente_var, data_inicio_frame, data_fim_frame, mes_ano_frame)
        ).grid(row=row, column=0, sticky=tk.W, pady=5)
        row += 1
        
        # Frame para data de início
        data_inicio_frame = ttk.Frame(form_frame)
        data_inicio_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        ttk.Label(
            data_inicio_frame, 
            text="Data de Início:"
        ).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        data_inicio_var = tk.StringVar(value=conta.get('data_inicio', datetime.datetime.now().strftime("%d/%m/%Y")))
        ttk.Entry(
            data_inicio_frame, 
            textvariable=data_inicio_var, 
            width=10
        ).grid(row=0, column=1, sticky=tk.W, pady=5)
        row += 1
        
        # Frame para data de fim
        data_fim_frame = ttk.Frame(form_frame)
        data_fim_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        ttk.Label(
            data_fim_frame, 
            text="Data de Fim (opcional):"
        ).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        data_fim_var = tk.StringVar(value=conta.get('data_fim', ''))
        ttk.Entry(
            data_fim_frame, 
            textvariable=data_fim_var, 
            width=10
        ).grid(row=0, column=1, sticky=tk.W, pady=5)
        row += 1
        
        # Frame para mês e ano
        mes_ano_frame = ttk.Frame(form_frame)
        mes_ano_frame.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=5)
        
        # Mês
        ttk.Label(
            mes_ano_frame, 
            text="Mês:"
        ).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        mes_var = tk.StringVar(value=str(conta.get('mes', datetime.datetime.now().month)))
        meses = [str(i) for i in range(1, 13)]
        ttk.Combobox(
            mes_ano_frame, 
            textvariable=mes_var, 
            values=meses, 
            width=3,
            state="readonly"
        ).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Ano
        ttk.Label(
            mes_ano_frame, 
            text="Ano:"
        ).grid(row=0, column=2, sticky=tk.W, pady=5, padx=(10, 0))
        
        ano_atual = datetime.datetime.now().year
        ano_var = tk.StringVar(value=str(conta.get('ano', ano_atual)))
        anos = [str(i) for i in range(ano_atual - 5, ano_atual + 6)]
        ttk.Combobox(
            mes_ano_frame, 
            textvariable=ano_var, 
            values=anos, 
            width=5,
            state="readonly"
        ).grid(row=0, column=3, sticky=tk.W, pady=5)
        row += 1
        
        # Novo campo: Data limite de pagamento
        ttk.Label(
            form_frame, 
            text="Dia de Vencimento:"
        ).grid(row=row, column=0, sticky=tk.W, pady=5)

        data_limite_var = tk.StringVar(value=conta.get('data_limite', ''))
        ttk.Entry(
            form_frame, 
            textvariable=data_limite_var, 
            width=10
        ).grid(row=row, column=1, sticky=tk.W, pady=5)

        # Adicionando um botão de ajuda para explicar o campo
        ttk.Button(
            form_frame,
            text="?",
            width=2,
            command=lambda: messagebox.showinfo(
                "Ajuda", 
                "Informe o dia do mês em que esta conta vence (1-31).\n"
                "Você também pode informar uma data completa no formato DD/MM/AAAA.\n"
                "O sistema irá lembrá-lo quando a data estiver próxima."
            )
        ).grid(row=row, column=1, sticky=tk.E, pady=5)
        row += 1
        
        # Variável para controlar se a conta é parcelada
        parcelado_var = tk.BooleanVar(value=conta.get('parcelado', False))
        
        # Checkbox para marcar como parcelada
        ttk.Checkbutton(
            form_frame,
            text="Conta Parcelada",
            variable=parcelado_var,
            command=lambda: self.atualizar_campos_parcelamento(form_frame, parcelado_var, parcelamento_frame, data_fim_frame, recorrente_var)
        ).grid(row=row, column=0, sticky=tk.W, pady=5)
        row += 1
        
        # Frame para opções de parcelamento
        parcelamento_frame = ttk.Frame(form_frame)
        parcelamento_frame.grid(row=row, column=0, columnspan=2, sticky=tk.EW, pady=5)
        row += 1
        
        # Número de parcelas
        ttk.Label(
            parcelamento_frame,
            text="Número de Parcelas:"
        ).grid(row=0, column=0, sticky=tk.W, pady=2)
        
        num_parcelas_var = tk.StringVar(value=str(conta.get('num_parcelas', 1)))
        ttk.Spinbox(
            parcelamento_frame,
            from_=1,
            to=99,
            textvariable=num_parcelas_var,
            width=5
        ).grid(row=0, column=1, sticky=tk.W, pady=2)
        
        # Opção de juros
        tem_juros_var = tk.BooleanVar(value='valor_com_juros' in conta)
        ttk.Checkbutton(
            parcelamento_frame,
            text="Incluir Juros",
            variable=tem_juros_var,
            command=lambda: self.atualizar_campos_juros(parcelamento_frame, tem_juros_var, juros_frame, valor_var, valor_com_juros_var)
        ).grid(row=1, column=0, sticky=tk.W, pady=2)
        
        # Frame para opções de juros
        juros_frame = ttk.Frame(parcelamento_frame)
        juros_frame.grid(row=2, column=0, columnspan=2, sticky=tk.EW, pady=2)
        
        # Valor total com juros
        ttk.Label(
            juros_frame,
            text="Valor Total com Juros (R$):"
        ).grid(row=0, column=0, sticky=tk.W, pady=2)
        
        valor_com_juros_var = tk.StringVar(value=str(conta.get('valor_com_juros', conta.get('valor', 0))))
        ttk.Entry(
            juros_frame,
            textvariable=valor_com_juros_var,
            width=10
        ).grid(row=0, column=1, sticky=tk.W, pady=2)
        
        # Configurando a visibilidade inicial dos campos
        if recorrente_var.get():
            mes_ano_frame.grid_remove()
        else:
            data_inicio_frame.grid_remove()
            data_fim_frame.grid_remove()
            mes_ano_frame.grid()
        
        if parcelado_var.get():
            parcelamento_frame.grid()
            
            # Se for parcelado e recorrente, oculta o campo de data de fim
            if recorrente_var.get():
                data_fim_frame.grid_remove()
        else:
            parcelamento_frame.grid_remove()
        
        if tem_juros_var.get():
            juros_frame.grid()
        else:
            juros_frame.grid_remove()
        
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
            command=lambda: self.atualizar_conta(
                formulario,
                conta_id,
                descricao_var.get(),
                valor_var.get(),
                recorrente_var.get(),
                data_inicio_var.get() if recorrente_var.get() else None,
                data_fim_var.get() if recorrente_var.get() and data_fim_var.get() else None,
                int(mes_var.get()) if not recorrente_var.get() else None,
                int(ano_var.get()) if not recorrente_var.get() else None,
                parcelado_var.get(),
                int(num_parcelas_var.get()) if parcelado_var.get() else None,
                tem_juros_var.get() if parcelado_var.get() else False,
                valor_com_juros_var.get() if parcelado_var.get() and tem_juros_var.get() else None,
                data_limite_var.get()  # Novo parâmetro
            )
        ).pack(side=tk.RIGHT)

    def atualizar_conta(self, formulario, conta_id, descricao, valor, recorrente, data_inicio, data_fim, mes, ano, parcelado, num_parcelas, tem_juros, valor_com_juros, data_limite):
        """Atualiza uma conta fixa existente"""
        # Validando os campos
        if not descricao:
            messagebox.showerror("Erro", "A descrição é obrigatória!")
            return
        
        try:
            valor = float(valor)
            if valor <= 0:
                raise ValueError("O valor deve ser maior que zero!")
        except ValueError:
            messagebox.showerror("Erro", "O valor deve ser um número válido maior que zero!")
            return
        
        # Criando o dicionário da conta
        conta = {
            'id': conta_id,
            'descricao': descricao,
            'valor': valor,
            'recorrente': recorrente
        }
        
        # Adicionando campos específicos de acordo com o tipo de conta
        if recorrente:
            # Validando a data de início
            try:
                datetime.datetime.strptime(data_inicio, "%d/%m/%Y")
                conta['data_inicio'] = data_inicio
            except ValueError:
                messagebox.showerror("Erro", "A data de início deve estar no formato DD/MM/AAAA!")
                return
            
            # Adicionando a data de fim (se existir)
            if data_fim:
                try:
                    datetime.datetime.strptime(data_fim, "%d/%m/%Y")
                    conta['data_fim'] = data_fim
                except ValueError:
                    messagebox.showerror("Erro", "A data de fim deve estar no formato DD/MM/AAAA!")
                    return
        else:
            # Adicionando o mês e ano
            conta['mes'] = mes
            conta['ano'] = ano
        
        # Adicionando a data limite de pagamento (se existir)
        if data_limite:
            try:
                # Verificando se é apenas um número (dia)
                if data_limite.isdigit() and 1 <= int(data_limite) <= 31:
                    # Armazenando apenas o dia
                    conta['data_limite'] = data_limite
                else:
                    # Tentando interpretar como uma data completa
                    datetime.datetime.strptime(data_limite, "%d/%m/%Y")
                    conta['data_limite'] = data_limite
            except ValueError:
                messagebox.showerror("Erro", "A data limite deve ser um dia do mês (1-31) ou uma data completa no formato DD/MM/AAAA!")
                return
        
        # Adicionando informações de parcelamento
        if parcelado:
            conta['parcelado'] = True
            conta['num_parcelas'] = num_parcelas
            
            # Adicionando informações de juros
            if tem_juros:
                try:
                    valor_com_juros = float(valor_com_juros)
                    if valor_com_juros <= valor:
                        messagebox.showerror("Erro", "O valor com juros deve ser maior que o valor original!")
                        return
                    conta['valor_com_juros'] = valor_com_juros
                except ValueError:
                    messagebox.showerror("Erro", "O valor com juros deve ser um número válido!")
                    return
            
            # Calculando automaticamente a data de fim se for uma conta recorrente parcelada
            if recorrente and not data_fim:
                try:
                    # Convertendo a data de início para um objeto datetime
                    data_inicio_obj = datetime.datetime.strptime(data_inicio, "%d/%m/%Y")
                    
                    # Calculando a data de fim (data de início + número de parcelas meses)
                    data_fim_obj = data_inicio_obj
                    for _ in range(num_parcelas - 1):  # -1 porque a primeira parcela é na data de início
                        # Avançando um mês
                        mes = data_fim_obj.month + 1
                        ano = data_fim_obj.year
                        if mes > 12:
                            mes = 1
                            ano += 1
                        
                        # Ajustando o dia para o último dia do mês se necessário
                        ultimo_dia = calendar.monthrange(ano, mes)[1]
                        dia = min(data_fim_obj.day, ultimo_dia)
                        
                        # Criando a nova data
                        data_fim_obj = datetime.datetime(ano, mes, dia)
                    
                    # Formatando a data de fim
                    conta['data_fim'] = data_fim_obj.strftime("%d/%m/%Y")
                    
                except Exception as e:
                    # Se ocorrer algum erro, apenas não define a data de fim
                    pass
        
        # Atualizando a conta
        self.data_manager.atualizar_conta_fixa(conta_id, conta)
        
        # Fechando o formulário
        formulario.destroy()
        
        # Atualizando a tabela
        self.atualizar()

    def excluir_conta(self, conta_id):
        """Exclui uma conta fixa"""
        # Confirmando a exclusão
        if messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir esta conta fixa?"):
            # Excluindo a conta
            self.data_manager.excluir_conta_fixa(conta_id)
            
            # Atualizando a tabela
            self.atualizar()
