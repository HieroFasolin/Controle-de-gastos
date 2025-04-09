"""
Aplicativo de Controle de Gastos
"""
import tkinter as tk
from tkinter import ttk, Menu, filedialog, messagebox
import os
import json
import datetime
import sys

# Importando os módulos do aplicativo
from models.data_manager import DataManager
from views.contas_fixas import ContasFixasFrame
from views.receitas import ReceitasFrame
from views.gastos_gerais import GastosGeraisFrame
from views.historico import HistoricoFrame
from views.visao_geral import VisaoGeralFrame

class ControleGastosApp(tk.Tk):
    """Classe principal do aplicativo de controle de gastos"""

    def __init__(self, modo_teste=False):
        """Inicializa o aplicativo"""
        super().__init__()
        
        # Define o modo (teste ou produção)
        self.modo_teste = modo_teste
        
        # Configurando a janela principal
        self.title(f"Controle Financeiro{' - MODO TESTE' if self.modo_teste else ''}")
        self.geometry("1000x650")
        self.minsize(800, 600)
        
        # Configurando o tema tradicional
        self.configurar_tema()
        
        # Inicializando o gerenciador de dados com o modo apropriado
        self.data_manager = DataManager(modo_teste=self.modo_teste)
        
        # Criando o menu
        self.criar_menu()
        
        # Criando o notebook (abas)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Criando as abas
        self.criar_abas()
        
        # Configurando o evento de fechamento da janela
        self.protocol("WM_DELETE_WINDOW", self.ao_fechar)
        
        # Configurando o evento de mudança de aba
        self.notebook.bind("<<NotebookTabChanged>>", self.ao_mudar_aba)
        
        # Indicador visual de modo teste
        if self.modo_teste:
            self.criar_indicador_teste()
            
        # Verificando contas não pagas e exibindo lembretes
        self.verificar_contas_nao_pagas()

    def verificar_contas_nao_pagas(self):
        """Verifica se existem contas não pagas e exibe lembretes"""
        # Obtendo o mês e ano atuais
        hoje = datetime.datetime.now()
        mes_atual = hoje.month
        ano_atual = hoje.year
        
        # Obtendo as contas fixas do período atual
        contas_fixas = self.data_manager.obter_contas_fixas_por_periodo(mes_atual, ano_atual)
        
        # Filtrando apenas as contas não pagas e com data limite próxima
        contas_nao_pagas = []
        for conta in contas_fixas:
            # Verificando se a conta não está paga
            if not conta.get('pago', False):
                # Verificando se tem data limite
                if 'data_limite' in conta:
                    try:
                        data_limite = datetime.datetime.strptime(conta['data_limite'], "%d/%m/%Y")
                        dias_restantes = (data_limite - hoje).days
                        
                        # Se faltam menos de 5 dias ou já passou da data
                        if dias_restantes <= 5:
                            status = "ATRASADA!" if dias_restantes < 0 else f"Vence em {dias_restantes} dias"
                            contas_nao_pagas.append((conta['descricao'], conta['data_limite'], status))
                    except ValueError:
                        # Se a data estiver em formato inválido, inclui sem calcular dias
                        contas_nao_pagas.append((conta['descricao'], conta.get('data_limite', 'Data desconhecida'), ""))
                else:
                    # Se não tiver data limite, inclui sem data
                    contas_nao_pagas.append((conta['descricao'], "Sem data limite", ""))
        
        # Se houver contas não pagas, exibe um lembrete
        if contas_nao_pagas:
            # Criando a mensagem
            mensagem = "Você tem as seguintes contas pendentes:\n\n"
            for descricao, data_limite, status in contas_nao_pagas:
                mensagem += f"• {descricao} - {data_limite} {status}\n"
            
            # Exibindo o lembrete
            messagebox.showwarning("Lembrete de Contas", mensagem)

    def configurar_tema(self):
        """Configura o tema visual do aplicativo"""
        # Configurando estilos personalizados para um visual tradicional
        self.style = ttk.Style()
        
        # Configurando cores de fundo e fonte para um visual tradicional
        bg_color = "#f0f0f0"
        header_bg = "#e1e1e1"
        
        # Estilo para títulos
        self.style.configure(
            "Title.TLabel",
            font=("Arial", 12, "bold"),
            background=bg_color
        )
        
        # Estilo para cabeçalhos
        self.style.configure(
            "Header.TLabel",
            font=("Arial", 10, "bold"),
            background=bg_color
        )
        
        # Estilo para frames
        self.style.configure(
            "TFrame",
            background=bg_color
        )
        
        # Estilo para botões
        self.style.configure(
            "TButton",
            font=("Arial", 9)
        )
        
        # Estilo para o notebook
        self.style.configure(
            "TNotebook",
            background=bg_color
        )
        
        self.style.configure(
            "TNotebook.Tab",
            font=("Arial", 9),
            padding=[10, 2]
        )
        
        # Estilo para Treeview (tabelas)
        self.style.configure(
            "Treeview",
            font=("Arial", 9),
            background="white",
            fieldbackground="white"
        )
        
        self.style.configure(
            "Treeview.Heading",
            font=("Arial", 9, "bold"),
            background=header_bg
        )
        
        # Configurando o fundo da janela principal
        self.configure(background=bg_color)

    def criar_indicador_teste(self):
        """Cria um indicador visual para o modo de teste"""
        frame_indicador = tk.Frame(self, bg="#ffcc00")
        frame_indicador.pack(fill=tk.X, side=tk.BOTTOM)
        
        label = tk.Label(
            frame_indicador, 
            text="MODO TESTE - Os dados não afetarão sua versão de produção", 
            bg="#ffcc00", 
            fg="black",
            font=("Arial", 9, "bold"),
            pady=2
        )
        label.pack()

    def criar_menu(self):
        """Cria o menu do aplicativo"""
        # Criando a barra de menu
        self.menubar = Menu(self)
        
        # Menu Arquivo
        file_menu = Menu(self.menubar, tearoff=0)
        file_menu.add_command(label="Alternar Modo", command=self.alternar_modo)
        file_menu.add_separator()
        file_menu.add_command(label="Sair", command=self.ao_fechar)
        self.menubar.add_cascade(label="Arquivo", menu=file_menu)
        
        # Menu Ajuda
        help_menu = Menu(self.menubar, tearoff=0)
        help_menu.add_command(label="Sobre", command=self.mostrar_sobre)
        self.menubar.add_cascade(label="Ajuda", menu=help_menu)
        
        # Configurando o menu
        self.config(menu=self.menubar)

    def alternar_modo(self):
        """Alterna entre modo teste e produção"""
        if messagebox.askyesno(
            "Alternar Modo", 
            f"Deseja alternar para o modo {'PRODUÇÃO' if self.modo_teste else 'TESTE'}?\n\n"
            "O aplicativo será reiniciado."
        ):
            # Salvar dados antes de alternar
            self.salvar_dados_atuais()
            
            # Reiniciar o aplicativo com o modo alternado
            python = sys.executable
            modo = "" if self.modo_teste else "--teste"
            os.execl(python, python, *sys.argv[0:1], modo)

    def criar_abas(self):
        """Cria as abas do aplicativo"""
        # Aba Visão Geral
        self.visao_geral_frame = VisaoGeralFrame(self.notebook, self.data_manager)
        self.notebook.add(self.visao_geral_frame, text="Visão Geral")
        
        # Aba Receitas
        self.receitas_frame = ReceitasFrame(self.notebook, self.data_manager)
        self.notebook.add(self.receitas_frame, text="Receitas")
        
        # Aba Gastos Gerais
        self.gastos_gerais_frame = GastosGeraisFrame(self.notebook, self.data_manager)
        self.notebook.add(self.gastos_gerais_frame, text="Gastos Gerais")
        
        # Aba Contas Fixas
        self.contas_fixas_frame = ContasFixasFrame(self.notebook, self.data_manager)
        self.notebook.add(self.contas_fixas_frame, text="Contas Fixas")
        
        # Aba Histórico
        self.historico_frame = HistoricoFrame(self.notebook, self.data_manager)
        self.notebook.add(self.historico_frame, text="Histórico")

    def ao_mudar_aba(self, event=None):
        """Método chamado quando o usuário muda de aba"""
        # Obtendo o índice da aba selecionada
        tab_index = self.notebook.index("current")
        
        # Atualizando a aba selecionada
        if tab_index == 0:  # Visão Geral
            self.visao_geral_frame.atualizar()
        elif tab_index == 1:  # Receitas
            self.receitas_frame.atualizar()
        elif tab_index == 2:  # Gastos Gerais
            self.gastos_gerais_frame.atualizar()
        elif tab_index == 3:  # Contas Fixas
            self.contas_fixas_frame.atualizar()
        elif tab_index == 4:  # Histórico
            self.historico_frame.atualizar()

    def mostrar_sobre(self):
        """Mostra informações sobre o aplicativo"""
        # Criando a janela "Sobre"
        sobre_window = tk.Toplevel(self)
        sobre_window.title("Sobre o Controle Financeiro")
        sobre_window.geometry("400x300")
        sobre_window.resizable(False, False)
        sobre_window.transient(self)
        sobre_window.grab_set()
        
        # Adicionando o conteúdo
        frame = ttk.Frame(sobre_window, padding=15)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        ttk.Label(
            frame, 
            text="Controle Financeiro", 
            font=("Arial", 14, "bold")
        ).pack(pady=(0, 5))
        
        # Versão
        ttk.Label(
            frame, 
            text="Versão 1.0.0",
            font=("Arial", 9)
        ).pack(pady=(0, 15))
        
        # Descrição
        ttk.Label(
            frame, 
            text="Aplicativo para controle de gastos pessoais.",
            wraplength=350,
            justify="center",
            font=("Arial", 9)
        ).pack(pady=(0, 10))
        
        # Desenvolvido por
        ttk.Label(
            frame, 
            text="Desenvolvido por: Hiero Fasolin Koboyama",
            wraplength=350,
            justify="center",
            font=("Arial", 9)
        ).pack(pady=(0, 10))
        
        # Ano
        ttk.Label(
            frame, 
            text=f"© {datetime.datetime.now().year} - Todos os direitos reservados.",
            wraplength=350,
            justify="center",
            font=("Arial", 8)
        ).pack(pady=(0, 15))
        
        # Botão Fechar
        ttk.Button(
            frame, 
            text="Fechar", 
            command=sobre_window.destroy,
            width=10
        ).pack(pady=(10, 0))

    def salvar_dados_atuais(self):
        """Salva os dados atuais"""
        try:
            # Obtendo os dados atuais
            gastos = self.data_manager.obter_gastos()
            receitas = self.data_manager.obter_receitas()
            contas_fixas = self.data_manager.obter_contas_fixas()
            
            # Salvando cada tipo de dado no seu respectivo arquivo
            self.data_manager.salvar_dados(self.data_manager.gastos_file, gastos)
            self.data_manager.salvar_dados(self.data_manager.receitas_file, receitas)
            self.data_manager.salvar_dados(self.data_manager.contas_fixas_file, contas_fixas)
            
            print("Dados salvos com sucesso!")
            
        except Exception as e:
            print(f"Erro ao salvar dados: {str(e)}")
            messagebox.showwarning("Aviso", "Não foi possível salvar os dados automaticamente. Seus dados podem ser perdidos.")

    def ao_fechar(self):
        """Método chamado quando o usuário fecha a janela"""
        try:
            # Confirmando o fechamento
            if messagebox.askyesno("Confirmar", "Deseja realmente sair do aplicativo?"):
                try:
                    # Salvando os dados automaticamente
                    self.salvar_dados_atuais()
                finally:
                    # Garantindo que o aplicativo será fechado
                    self.quit()
                    self.destroy()
        except Exception as e:
            print(f"Erro ao fechar o aplicativo: {str(e)}")
            # Forçando o fechamento mesmo em caso de erro
            self.quit()
            self.destroy()

# Função principal
def main():
    """Função principal do aplicativo"""
    # Verifica se o modo teste foi solicitado via linha de comando
    modo_teste = "--teste" in sys.argv
    
    app = ControleGastosApp(modo_teste=modo_teste)
    app.mainloop()

# Executando o aplicativo
if __name__ == "__main__":
    main()
