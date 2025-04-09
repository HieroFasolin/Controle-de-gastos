"""
Módulo de visualização da aba Histórico
"""
import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import os
import sys

class HistoricoFrame(ttk.Frame):
    """Frame para a aba de Histórico"""
    
    def __init__(self, parent, data_manager):
        """Inicializa o frame de Histórico"""
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
            text="Histórico Financeiro", 
            style="Title.TLabel"
        )
        titulo_label.pack(side=tk.LEFT)
        
        # Frame para seleção de período
        periodo_frame = ttk.Frame(titulo_frame)
        periodo_frame.pack(side=tk.RIGHT)
        
        # Obtendo o mês e ano atuais
        hoje = datetime.datetime.now()
        self.mes_atual = hoje.month
        self.ano_atual = hoje.year
        
        # Variáveis para o mês e ano selecionados
        self.filtro_mes_var = tk.StringVar(value=str(self.mes_atual))
        self.filtro_ano_var = tk.StringVar(value=str(self.ano_atual))
        
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
        anos = [str(i) for i in range(hoje.year - 5, hoje.year + 2)]
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
        tabela_frame = ttk.Frame(self)
        tabela_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Criando a tabela (Treeview)
        colunas = ('tipo', 'descricao', 'categoria', 'valor', 'data', 'status', 'parcelas')
        self.tabela = ttk.Treeview(
            tabela_frame, 
            columns=colunas, 
            show='headings',
            selectmode='browse'
        )
        
        # Configurando as colunas
        self.tabela.heading('tipo', text='Tipo')
        self.tabela.heading('descricao', text='Descrição')
        self.tabela.heading('categoria', text='Categoria')
        self.tabela.heading('valor', text='Valor (R$)')
        self.tabela.heading('data', text='Data')
        self.tabela.heading('status', text='Status')
        self.tabela.heading('parcelas', text='Parcelas')
        
        # Configurando a largura das colunas
        self.tabela.column('tipo', width=100)
        self.tabela.column('descricao', width=200)
        self.tabela.column('categoria', width=150)
        self.tabela.column('valor', width=100)
        self.tabela.column('data', width=100)
        self.tabela.column('status', width=100)
        self.tabela.column('parcelas', width=80)
        
        # Adicionando a tabela ao frame com scrollbar
        self.tabela.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tabela_frame, orient=tk.VERTICAL, command=self.tabela.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tabela.configure(yscrollcommand=scrollbar.set)
        
        # Adicionando menu de contexto para contas fixas
        self.tabela.bind("<Button-3>", self.abrir_menu_contexto)
        
        # Frame para os botões
        botoes_frame = ttk.Frame(self)
        botoes_frame.pack(fill=tk.X, pady=10)
        
        # Botão para marcar conta fixa como paga
        ttk.Button(
            botoes_frame,
            text="Marcar Conta como Paga",
            command=self.marcar_conta_como_paga
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        # Botão para marcar conta fixa como pendente
        ttk.Button(
            botoes_frame,
            text="Marcar Conta como Pendente",
            command=self.marcar_conta_como_pendente
        ).pack(side=tk.LEFT, padx=5)
        
        # Botão para atualizar
        ttk.Button(
            botoes_frame,
            text="Atualizar Lista",
            command=self.atualizar
        ).pack(side=tk.RIGHT)
        
        # Frame para o resumo
        resumo_frame = ttk.Frame(self)
        resumo_frame.pack(fill=tk.X, pady=10)
        
        # Título do resumo
        ttk.Label(
            resumo_frame, 
            text="Resumo do Período", 
            style="Header.TLabel"
        ).pack(fill=tk.X, pady=(0, 10))
        
        # Frame para os valores
        valores_frame = ttk.Frame(resumo_frame)
        valores_frame.pack(fill=tk.X)
        
        # Criando os labels para os valores
        # Total de Gastos
        ttk.Label(
            valores_frame, 
            text="Total de Gastos:", 
            anchor=tk.W
        ).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.total_gastos_label = ttk.Label(
            valores_frame, 
            text="R$ 0,00", 
            anchor=tk.E
        )
        self.total_gastos_label.grid(row=0, column=1, sticky=tk.E, pady=5)
        
        # Total de Receitas
        ttk.Label(
            valores_frame, 
            text="Total de Receitas:", 
            anchor=tk.W
        ).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.total_receitas_label = ttk.Label(
            valores_frame, 
            text="R$ 0,00", 
            anchor=tk.E
        )
        self.total_receitas_label.grid(row=1, column=1, sticky=tk.E, pady=5)
        
        # Total de Contas Fixas
        ttk.Label(
            valores_frame, 
            text="Total de Contas Fixas:", 
            anchor=tk.W
        ).grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.total_contas_fixas_label = ttk.Label(
            valores_frame, 
            text="R$ 0,00", 
            anchor=tk.E
        )
        self.total_contas_fixas_label.grid(row=2, column=1, sticky=tk.E, pady=5)
        
        # Separador
        ttk.Separator(valores_frame, orient=tk.HORIZONTAL).grid(
            row=3, column=0, columnspan=2, sticky=tk.EW, pady=10
        )
        
        # Saldo
        ttk.Label(
            valores_frame, 
            text="Saldo:", 
            anchor=tk.W,
            style="Header.TLabel"
        ).grid(row=4, column=0, sticky=tk.W, pady=5)
        
        self.saldo_label = ttk.Label(
            valores_frame, 
            text="R$ 0,00", 
            anchor=tk.E,
            style="Header.TLabel"
        )
        self.saldo_label.grid(row=4, column=1, sticky=tk.E, pady=5)
        
        # Configurando o grid
        valores_frame.columnconfigure(0, weight=1)
        valores_frame.columnconfigure(1, weight=1)

    def atualizar(self, event=None):
        """Atualiza os dados da tabela"""
        try:
            # Obtendo o mês e ano selecionados
            mes = int(self.filtro_mes_var.get())
            ano = int(self.filtro_ano_var.get())
            
            # Limpando a tabela
            for item in self.tabela.get_children():
                self.tabela.delete(item)
            
            # Obtendo os dados para o histórico
            dados_historico = self.data_manager.obter_dados_para_historico(mes, ano)
            
            # Adicionando os dados à tabela
            for dado in dados_historico:
                # Formatando o valor
                valor_original = float(dado['valor'])
                parcelas_info = ""
                
                # Verificando se é uma conta fixa parcelada
                if dado['tipo'] == 'Conta Fixa' and dado.get('parcelado', False):
                    num_parcelas = int(dado.get('num_parcelas', 1))
                    
                    # Verificando se tem juros
                    if 'valor_com_juros' in dado:
                        valor_com_juros = float(dado['valor_com_juros'])
                        valor_sem_juros = float(dado['valor_sem_juros'])
                        
                        # Calculando o valor da parcela com juros
                        valor_parcela = valor_com_juros / num_parcelas
                        
                        # Calculando o valor dos juros por parcela
                        juros_total = valor_com_juros - valor_sem_juros
                        juros_por_parcela = juros_total / num_parcelas
                        
                        # Formatando o valor da parcela
                        valor = f"R$ {valor_parcela:.2f}"
                        
                        # Adicionando informação de juros ao status
                        if juros_total > 0:
                            status = dado.get('status', '-')
                            status += f" (Juros: R$ {juros_por_parcela:.2f})"
                            dado['status'] = status
                    else:
                        # Calculando o valor da parcela sem juros
                        valor_parcela = valor_original / num_parcelas
                        valor = f"R$ {valor_parcela:.2f}"
                    
                    # Informação de parcelas
                    if 'data_inicio' in dado:
                        data_inicio = datetime.datetime.strptime(dado['data_inicio'], "%d/%m/%Y")
                        mes_inicio = data_inicio.month
                        ano_inicio = data_inicio.year
                        
                        # Calculando o número da parcela atual
                        meses_passados = (ano - ano_inicio) * 12 + (mes - mes_inicio)
                        parcela_atual = meses_passados + 1  # Começando em 1, não em 0
                        
                        if 1 <= parcela_atual <= num_parcelas:
                            parcelas_info = f"{parcela_atual}/{num_parcelas}"
                        else:
                            parcelas_info = f"{num_parcelas}x"
                    else:
                        parcelas_info = f"{num_parcelas}x"
                else:
                    valor = f"R$ {valor_original:.2f}"
                
                # Formatando o status (se existir)
                status = dado.get('status', '-')
                
                # Definindo a cor da linha com base no tipo
                tag = dado['tipo'].lower()
                
                self.tabela.insert(
                    '', 
                    'end', 
                    values=(
                        dado['tipo'],
                        dado['descricao'],
                        dado['categoria'],
                        valor,
                        dado['data'],
                        status,
                        parcelas_info
                    ),
                    tags=(dado.get('id', ''), dado['tipo'], tag)
                )
            
            # Configurando as cores das linhas
            self.tabela.tag_configure('gasto', background='#ffcccc')
            self.tabela.tag_configure('receita', background='#ccffcc')
            self.tabela.tag_configure('conta fixa', background='#cce5ff')
            self.tabela.tag_configure('pago', background='#e6ffe6')  # Verde claro
            
            # Atualizando o resumo
            self.atualizar_resumo(mes, ano)
            
        except (ValueError, TypeError) as e:
            messagebox.showerror("Erro", f"Erro ao atualizar o histórico: {str(e)}")
    
    def atualizar_resumo(self, mes, ano):
        """Atualiza o resumo financeiro"""
        # Obtendo os dados
        gastos = self.data_manager.obter_gastos_por_periodo(mes, ano)
        receitas = self.data_manager.obter_receitas_por_periodo(mes, ano)
        contas_fixas = self.data_manager.obter_contas_fixas_por_periodo(mes, ano)
        
        # Calculando os totais
        total_gastos = self.data_manager.calcular_total_gastos(gastos)
        total_receitas = self.data_manager.calcular_total_receitas(receitas)
        
        # Calculando o total de contas fixas considerando parcelas
        total_contas_fixas = self.calcular_total_contas_fixas_com_parcelas(contas_fixas, mes, ano)
        
        saldo = total_receitas - total_gastos - total_contas_fixas
        
        # Atualizando os labels
        self.total_gastos_label.config(text=f"R$ {total_gastos:.2f}")
        self.total_receitas_label.config(text=f"R$ {total_receitas:.2f}")
        self.total_contas_fixas_label.config(text=f"R$ {total_contas_fixas:.2f}")
        
        # Atualizando o saldo com cor
        self.saldo_label.config(
            text=f"R$ {saldo:.2f}",
            foreground="green" if saldo >= 0 else "red"
        )
    
    def calcular_total_contas_fixas_com_parcelas(self, contas_fixas, mes, ano):
        """Calcula o total de contas fixas considerando parcelas"""
        total = 0.0
        
        for conta in contas_fixas:
            valor_original = float(conta['valor'])
            
            # Verificando se a conta é parcelada
            if conta.get('parcelado', False):
                num_parcelas = int(conta.get('num_parcelas', 1))
                
                # Verificando se tem juros
                if 'valor_com_juros' in conta:
                    valor_com_juros = float(conta['valor_com_juros'])
                    
                    # Calculando o valor da parcela com juros
                    valor_parcela = valor_com_juros / num_parcelas
                else:
                    # Calculando o valor da parcela sem juros
                    valor_parcela = valor_original / num_parcelas
                
                # Verificando se a parcela atual está dentro do período válido
                if 'data_inicio' in conta:
                    data_inicio = datetime.datetime.strptime(conta['data_inicio'], "%d/%m/%Y")
                    mes_inicio = data_inicio.month
                    ano_inicio = data_inicio.year
                    
                    # Calculando o número da parcela atual
                    meses_passados = (ano - ano_inicio) * 12 + (mes - mes_inicio)
                    parcela_atual = meses_passados + 1  # Começando em 1, não em 0
                    
                    # Só adiciona ao total se a parcela atual estiver dentro do período válido
                    if 1 <= parcela_atual <= num_parcelas:
                        total += valor_parcela
                else:
                    # Se não tiver data de início, considera o valor da parcela
                    total += valor_parcela
            else:
                # Se não for parcelada, adiciona o valor total
                total += valor_original
        
        return total
    
    def abrir_menu_contexto(self, event):
        """Abre o menu de contexto ao clicar com o botão direito"""
        # Obtendo o item selecionado
        item = self.tabela.identify_row(event.y)
        
        if item:
            # Selecionando o item
            self.tabela.selection_set(item)
            
            # Obtendo o tipo do item
            tags = self.tabela.item(item, 'tags')
            if len(tags) >= 2:
                tipo = tags[1]
                
                # Se for uma conta fixa, exibe o menu de contexto
                if tipo == 'Conta Fixa':
                    # Obtendo o ID da conta
                    conta_id = int(tags[0])
                    
                    # Obtendo o mês e ano selecionados
                    mes = int(self.filtro_mes_var.get())
                    ano = int(self.filtro_ano_var.get())
                    
                    # Verificando se a conta está paga
                    pago = self.data_manager.verificar_conta_paga(conta_id, mes, ano)
                    
                    # Criando o menu de contexto
                    menu = tk.Menu(self, tearoff=0)
                    
                    # Adicionando opções para marcar como pago/pendente
                    if pago:
                        menu.add_command(label="Marcar como Pendente", 
                                        command=lambda: self.marcar_como_pendente_menu(conta_id, mes, ano))
                    else:
                        menu.add_command(label="Marcar como Pago", 
                                        command=lambda: self.marcar_como_pago_menu(conta_id, mes, ano))
                    
                    # Exibindo o menu
                    menu.post(event.x_root, event.y_root)

    def marcar_conta_como_paga(self):
        """Marca a conta fixa selecionada como paga"""
        # Obtendo o item selecionado
        selecao = self.tabela.selection()
        
        if not selecao:
            messagebox.showwarning("Aviso", "Nenhum item selecionado!")
            return
        
        item = selecao[0]
        tags = self.tabela.item(item, 'tags')
        
        # Verificando se é uma conta fixa
        if len(tags) >= 2 and tags[1] == 'Conta Fixa':
            # Obtendo o ID da conta
            conta_id = int(tags[0])
            
            # Obtendo o mês e ano selecionados
            mes = int(self.filtro_mes_var.get())
            ano = int(self.filtro_ano_var.get())
            
            # Marcando a conta como paga
            self.data_manager.marcar_conta_como_paga(conta_id, mes, ano)
            
            # Atualizando a tabela
            self.atualizar()
            
            messagebox.showinfo("Sucesso", "Conta marcada como paga!")
        else:
            messagebox.showwarning("Aviso", "O item selecionado não é uma conta fixa!")

    def marcar_conta_como_pendente(self):
        """Marca a conta fixa selecionada como pendente"""
        # Obtendo o item selecionado
        selecao = self.tabela.selection()
        
        if not selecao:
            messagebox.showwarning("Aviso", "Nenhum item selecionado!")
            return
        
        item = selecao[0]
        tags = self.tabela.item(item, 'tags')
        
        # Verificando se é uma conta fixa
        if len(tags) >= 2 and tags[1] == 'Conta Fixa':
            # Obtendo o ID da conta
            conta_id = int(tags[0])
            
            # Obtendo o mês e ano selecionados
            mes = int(self.filtro_mes_var.get())
            ano = int(self.filtro_ano_var.get())
            
            # Marcando a conta como pendente
            self.data_manager.marcar_conta_como_paga(conta_id, mes, ano, status_pago=False)
            
            # Atualizando a tabela
            self.atualizar()
            
            messagebox.showinfo("Sucesso", "Conta marcada como pendente!")
        else:
            messagebox.showwarning("Aviso", "O item selecionado não é uma conta fixa!")

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
