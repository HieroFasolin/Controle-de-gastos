"""
Módulo de visualização da aba Visão Geral com interface tradicional
"""
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime

class VisaoGeralFrame(ttk.Frame):
    """Frame para a aba de Visão Geral"""
    
    def __init__(self, parent, data_manager):
        """Inicializa o frame de Visão Geral"""
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
        # Frame para o título
        titulo_frame = ttk.Frame(self)
        titulo_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Título
        titulo_label = ttk.Label(
            titulo_frame, 
            text="Visão Geral das Finanças", 
            style="Title.TLabel"
        )
        titulo_label.pack(side=tk.LEFT)
        
        # Seletor de mês/ano
        self.mes_var = tk.StringVar()
        self.ano_var = tk.StringVar()
        
        # Obtendo o mês e ano atuais
        hoje = datetime.datetime.now()
        self.mes_atual = hoje.month
        self.ano_atual = hoje.year
        
        # Configurando os valores iniciais
        self.mes_var.set(str(self.mes_atual))
        self.ano_var.set(str(self.ano_atual))
        
        # Frame para seleção de período
        periodo_frame = ttk.Frame(titulo_frame)
        periodo_frame.pack(side=tk.RIGHT)
        
        # Label para o mês
        ttk.Label(periodo_frame, text="Mês:").pack(side=tk.LEFT, padx=(0, 5))
        
        # Combobox para o mês
        meses = [str(i) for i in range(1, 13)]
        mes_combo = ttk.Combobox(
            periodo_frame, 
            textvariable=self.mes_var, 
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
            textvariable=self.ano_var, 
            values=anos, 
            width=5,
            state="readonly"
        )
        ano_combo.pack(side=tk.LEFT)
        
        # Configurando eventos
        mes_combo.bind("<<ComboboxSelected>>", self.atualizar)
        ano_combo.bind("<<ComboboxSelected>>", self.atualizar)
        
        # Frame principal dividido em duas colunas
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Coluna da esquerda (gráfico)
        grafico_frame = ttk.Frame(main_frame, relief=tk.GROOVE, borderwidth=1)
        grafico_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Frame para o gráfico
        self.grafico_container = ttk.Frame(grafico_frame, padding=5)
        self.grafico_container.pack(fill=tk.BOTH, expand=True)
        
        # Coluna da direita (resumo)
        resumo_frame = ttk.Frame(main_frame, relief=tk.GROOVE, borderwidth=1, width=250)
        resumo_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 0))
        resumo_frame.pack_propagate(False)  # Impede que o frame encolha
        
        # Título do resumo
        ttk.Label(
            resumo_frame, 
            text="Resumo Financeiro", 
            style="Header.TLabel",
            padding=(5, 5)
        ).pack(fill=tk.X)
        
        # Separador
        ttk.Separator(resumo_frame, orient=tk.HORIZONTAL).pack(fill=tk.X)
        
        # Frame para os valores
        valores_frame = ttk.Frame(resumo_frame, padding=10)
        valores_frame.pack(fill=tk.X)
        
        # Criando os labels para os valores
        # Receitas
        ttk.Label(
            valores_frame, 
            text="Receitas:", 
            anchor=tk.W
        ).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.receitas_label = ttk.Label(
            valores_frame, 
            text="R$ 0,00",
            anchor=tk.E
        )
        self.receitas_label.grid(row=0, column=1, sticky=tk.E, pady=5)
        
        # Gastos
        ttk.Label(
            valores_frame, 
            text="Gastos:", 
            anchor=tk.W
        ).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.gastos_label = ttk.Label(
            valores_frame, 
            text="R$ 0,00", 
            anchor=tk.E
        )
        self.gastos_label.grid(row=1, column=1, sticky=tk.E, pady=5)
        
        # Contas Fixas
        ttk.Label(
            valores_frame, 
            text="Contas Fixas:", 
            anchor=tk.W
        ).grid(row=2, column=0, sticky=tk.W, pady=5)
        
        self.contas_fixas_label = ttk.Label(
            valores_frame, 
            text="R$ 0,00", 
            anchor=tk.E
        )
        self.contas_fixas_label.grid(row=2, column=1, sticky=tk.E, pady=5)
        
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
        
        # Estatísticas adicionais
        ttk.Label(
            resumo_frame, 
            text="Estatísticas", 
            style="Header.TLabel",
            padding=(5, 5)
        ).pack(fill=tk.X, pady=(10, 0))
        
        # Separador
        ttk.Separator(resumo_frame, orient=tk.HORIZONTAL).pack(fill=tk.X)
        
        # Frame para as estatísticas
        stats_frame = ttk.Frame(resumo_frame, padding=10)
        stats_frame.pack(fill=tk.X)
        
        # Maior gasto
        ttk.Label(
            stats_frame, 
            text="Maior gasto:", 
            anchor=tk.W
        ).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.maior_gasto_label = ttk.Label(
            stats_frame, 
            text="N/A", 
            anchor=tk.E
        )
        self.maior_gasto_label.grid(row=0, column=1, sticky=tk.E, pady=5)
        
        # Categoria com mais gastos
        ttk.Label(
            stats_frame, 
            text="Categoria principal:", 
            anchor=tk.W
        ).grid(row=1, column=0, sticky=tk.W, pady=5)
        
        self.categoria_principal_label = ttk.Label(
            stats_frame, 
            text="N/A", 
            anchor=tk.E
        )
        self.categoria_principal_label.grid(row=1, column=1, sticky=tk.E, pady=5)
        
        # Configurando o grid
        stats_frame.columnconfigure(0, weight=1)
        stats_frame.columnconfigure(1, weight=1)
    
    def atualizar(self, event=None):
        """Atualiza os dados do frame"""
        try:
            mes = int(self.mes_var.get())
            ano = int(self.ano_var.get())
            
            # Atualizando os dados
            self.atualizar_resumo(mes, ano)
            self.atualizar_grafico(mes, ano)
            
        except (ValueError, TypeError):
            # Caso ocorra algum erro na conversão dos valores
            pass
    
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
        self.receitas_label.config(text=f"R$ {total_receitas:.2f}")
        self.gastos_label.config(text=f"R$ {total_gastos:.2f}")
        self.contas_fixas_label.config(text=f"R$ {total_contas_fixas:.2f}")
        
        # Atualizando o saldo com cor
        self.saldo_label.config(
            text=f"R$ {saldo:.2f}",
            foreground="green" if saldo >= 0 else "red"
        )
        
        # Atualizando estatísticas
        self.atualizar_estatisticas(gastos)
    
    def calcular_total_contas_fixas_com_parcelas(self, contas_fixas, mes, ano):
        """Calcula o total de contas fixas considerando parcelas"""
        total = 0.0
        
        for conta in contas_fixas:
            valor_original = float(conta['valor'])
            
            # Verificando se a conta é parcelada
            if conta.get('parcelado', False):
                num_parcelas = int(conta.get('num_parcelas', 1))
                
                # Calculando o valor da parcela
                valor_parcela = valor_original / num_parcelas
                
                # Adicionando apenas o valor da parcela
                total += valor_parcela
            else:
                # Se não for parcelada, adiciona o valor total
                total += valor_original
        
        return total
    
    def atualizar_estatisticas(self, gastos):
        """Atualiza as estatísticas"""
        if not gastos:
            self.maior_gasto_label.config(text="N/A")
            self.categoria_principal_label.config(text="N/A")
            return
        
        # Encontrando o maior gasto
        maior_gasto = max(gastos, key=lambda x: float(x['valor']))
        self.maior_gasto_label.config(
            text=f"{maior_gasto['descricao']} (R$ {float(maior_gasto['valor']):.2f})"
        )
        
        # Encontrando a categoria com mais gastos
        gastos_por_categoria = self.data_manager.obter_gastos_por_categoria(
            int(self.mes_var.get()), 
            int(self.ano_var.get())
        )
        
        if gastos_por_categoria:
            categoria_principal = max(
                gastos_por_categoria.items(), 
                key=lambda x: x[1]
            )
            self.categoria_principal_label.config(
                text=f"{categoria_principal[0]} (R$ {categoria_principal[1]:.2f})"
            )
        else:
            self.categoria_principal_label.config(text="N/A")
    
    def atualizar_grafico(self, mes, ano):
        """Atualiza o gráfico de pizza"""
        # Limpando o container do gráfico
        for widget in self.grafico_container.winfo_children():
            widget.destroy()
        
        # Obtendo os dados para o gráfico
        gastos_por_categoria = self.data_manager.obter_gastos_por_categoria(mes, ano)
        
        # Filtrando categorias com valor zero
        gastos_por_categoria = {k: v for k, v in gastos_por_categoria.items() if v > 0}
        
        if not gastos_por_categoria:
            # Se não houver dados, exibe uma mensagem
            ttk.Label(
                self.grafico_container, 
                text="Sem dados para exibir",
                font=("Arial", 10)
            ).pack(expand=True)
            return
        
        # Criando a figura
        plt.style.use('classic')
        fig, ax = plt.subplots(figsize=(6, 5), dpi=100)
        
        # Criando o gráfico de pizza
        labels = list(gastos_por_categoria.keys())
        sizes = list(gastos_por_categoria.values())
        
        # Cores para o gráfico (paleta clássica)
        colors = [
            '#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3', 
            '#fdb462', '#b3de69', '#fccde5', '#d9d9d9', '#bc80bd'
        ]
        
        # Destacando a maior fatia
        explode = [0.1 if i == sizes.index(max(sizes)) else 0 for i in range(len(sizes))]
        
        # Plotando o gráfico
        wedges, texts, autotexts = ax.pie(
            sizes, 
            explode=explode, 
            labels=labels, 
            colors=colors,
            autopct='%1.1f%%',
            shadow=True, 
            startangle=90,
            textprops={'fontsize': 9}
        )
        
        # Configurando o título
        ax.set_title(f'Distribuição de Gastos - {mes}/{ano}', fontsize=11)
        
        # Configurando a legenda
        ax.legend(
            wedges, 
            [f"{l} (R$ {s:.2f})" for l, s in zip(labels, sizes)],
            title="Categorias",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1),
            fontsize=8
        )
        
        # Ajustando o layout
        plt.tight_layout()
        
        # Criando o canvas para exibir o gráfico no Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.grafico_container)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
