"""
Módulo de gerenciamento de dados para o aplicativo de controle de gastos
"""
import os
import json
import datetime
import calendar
from datetime import datetime as dt

class DataManager:
    """Classe responsável pelo gerenciamento de dados do aplicativo"""
    
    def __init__(self, modo_teste=False):
        """Inicializa o gerenciador de dados"""
        # Define o modo (teste ou produção)
        self.modo_teste = modo_teste
        
        # Definindo os caminhos dos arquivos
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Diretório de dados baseado no modo
        if self.modo_teste:
            self.data_dir = os.path.join(base_dir, "data_teste")
        else:
            self.data_dir = os.path.join(base_dir, "data")
            
        # Definindo os arquivos de dados
        self.gastos_file = os.path.join(self.data_dir, "dados_gastos.json")
        self.receitas_file = os.path.join(self.data_dir, "receitas.json")
        self.contas_fixas_file = os.path.join(self.data_dir, "contas_fixas.json")
        
        # Criando os arquivos se não existirem
        self.verificar_arquivos()
        
        # Categorias de gastos
        self.categorias = [
            "Alimentação", 
            "Transporte", 
            "Moradia", 
            "Saúde", 
            "Educação", 
            "Lazer", 
            "Vestuário", 
            "Outros"
        ]
    
    def verificar_arquivos(self):
        """Verifica se os arquivos de dados existem, caso contrário, cria-os"""
        # Criando o diretório de dados se não existir
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Verificando e criando o arquivo de gastos
        if not os.path.exists(self.gastos_file):
            with open(self.gastos_file, 'w', encoding='utf-8') as f:
                json.dump([], f)
        
        # Verificando e criando o arquivo de receitas
        if not os.path.exists(self.receitas_file):
            with open(self.receitas_file, 'w', encoding='utf-8') as f:
                json.dump([], f)
        
        # Verificando e criando o arquivo de contas fixas
        if not os.path.exists(self.contas_fixas_file):
            with open(self.contas_fixas_file, 'w', encoding='utf-8') as f:
                json.dump([], f)
    
    def carregar_dados(self, arquivo):
        """Carrega os dados de um arquivo JSON"""
        try:
            with open(arquivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            # Se o arquivo estiver vazio ou não existir, retorna uma lista vazia
            return []
    
    def salvar_dados(self, arquivo, dados):
        """Salva os dados em um arquivo JSON"""
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)
    
    # Métodos para gerenciar gastos
    def obter_gastos(self):
        """Retorna todos os gastos"""
        return self.carregar_dados(self.gastos_file)
    
    def adicionar_gasto(self, gasto):
        """Adiciona um novo gasto"""
        gastos = self.obter_gastos()
        
        # Gerando um ID único para o gasto
        gasto['id'] = self._gerar_id(gastos)
        
        gastos.append(gasto)
        self.salvar_dados(self.gastos_file, gastos)
    
    def atualizar_gasto(self, gasto_id, gasto_atualizado):
        """Atualiza um gasto existente"""
        gastos = self.obter_gastos()
        
        for i, gasto in enumerate(gastos):
            if gasto['id'] == gasto_id:
                gasto_atualizado['id'] = gasto_id
                gastos[i] = gasto_atualizado
                break
        
        self.salvar_dados(self.gastos_file, gastos)
    
    def excluir_gasto(self, gasto_id):
        """Exclui um gasto"""
        gastos = self.obter_gastos()
        gastos = [g for g in gastos if g['id'] != gasto_id]
        self.salvar_dados(self.gastos_file, gastos)
    
    # Métodos para gerenciar receitas
    def obter_receitas(self):
        """Retorna todas as receitas"""
        return self.carregar_dados(self.receitas_file)
    
    def adicionar_receita(self, receita):
        """Adiciona uma nova receita"""
        receitas = self.obter_receitas()
        
        # Gerando um ID único para a receita
        receita['id'] = self._gerar_id(receitas)
        
        receitas.append(receita)
        self.salvar_dados(self.receitas_file, receitas)
    
    def atualizar_receita(self, receita_id, receita_atualizada):
        """Atualiza uma receita existente"""
        receitas = self.obter_receitas()
        
        for i, receita in enumerate(receitas):
            if receita['id'] == receita_id:
                receita_atualizada['id'] = receita_id
                receitas[i] = receita_atualizada
                break
        
        self.salvar_dados(self.receitas_file, receitas)
    
    def excluir_receita(self, receita_id):
        """Exclui uma receita"""
        receitas = self.obter_receitas()
        receitas = [r for r in receitas if r['id'] != receita_id]
        self.salvar_dados(self.receitas_file, receitas)
    
    # Métodos para gerenciar contas fixas
    def obter_contas_fixas(self):
        """Retorna todas as contas fixas"""
        return self.carregar_dados(self.contas_fixas_file)
    
    def adicionar_conta_fixa(self, conta):
        """Adiciona uma nova conta fixa"""
        contas = self.obter_contas_fixas()
        
        # Gerando um ID único para a conta
        conta['id'] = self._gerar_id(contas)
        
        # Verificando se é uma conta parcelada
        if 'parcelado' in conta and conta['parcelado']:
            # Definindo o número de parcelas
            conta['num_parcelas'] = int(conta.get('num_parcelas', 1))
            
            # Se for parcelada, a data de fim é calculada automaticamente
            if 'data_inicio' in conta:
                data_inicio = dt.strptime(conta['data_inicio'], "%d/%m/%Y")
                num_parcelas = int(conta['num_parcelas'])
                
                # Calculando a data de fim (data de início + número de parcelas - 1 mês)
                data_fim = data_inicio
                for _ in range(num_parcelas - 1):
                    # Avançando um mês
                    if data_fim.month == 12:
                        data_fim = dt(data_fim.year + 1, 1, data_fim.day)
                    else:
                        # Tratando casos onde o dia pode não existir no mês seguinte
                        ultimo_dia = calendar.monthrange(data_fim.year, data_fim.month + 1)[1]
                        dia = min(data_fim.day, ultimo_dia)
                        data_fim = dt(data_fim.year, data_fim.month + 1, dia)
                
                # Formatando a data de fim
                conta['data_fim'] = data_fim.strftime("%d/%m/%Y")
        
        contas.append(conta)
        self.salvar_dados(self.contas_fixas_file, contas)
    
    def atualizar_conta_fixa(self, conta_id, conta_atualizada):
        """Atualiza uma conta fixa existente"""
        contas = self.obter_contas_fixas()
        
        for i, conta in enumerate(contas):
            if conta['id'] == conta_id:
                conta_atualizada['id'] = conta_id
                
                # Verificando se é uma conta parcelada
                if 'parcelado' in conta_atualizada and conta_atualizada['parcelado']:
                    # Definindo o número de parcelas
                    conta_atualizada['num_parcelas'] = int(conta_atualizada.get('num_parcelas', 1))
                    
                    # Se for parcelada, a data de fim é calculada automaticamente
                    if 'data_inicio' in conta_atualizada:
                        data_inicio = dt.strptime(conta_atualizada['data_inicio'], "%d/%m/%Y")
                        num_parcelas = int(conta_atualizada['num_parcelas'])
                        
                        # Calculando a data de fim (data de início + número de parcelas - 1 mês)
                        data_fim = data_inicio
                        for _ in range(num_parcelas - 1):
                            # Avançando um mês
                            if data_fim.month == 12:
                                data_fim = dt(data_fim.year + 1, 1, data_fim.day)
                            else:
                                # Tratando casos onde o dia pode não existir no mês seguinte
                                ultimo_dia = calendar.monthrange(data_fim.year, data_fim.month + 1)[1]
                                dia = min(data_fim.day, ultimo_dia)
                                data_fim = dt(data_fim.year, data_fim.month + 1, dia)
                        
                        # Formatando a data de fim
                        conta_atualizada['data_fim'] = data_fim.strftime("%d/%m/%Y")
                
                contas[i] = conta_atualizada
                break
        
        self.salvar_dados(self.contas_fixas_file, contas)
    
    def excluir_conta_fixa(self, conta_id):
        """Exclui uma conta fixa"""
        contas = self.obter_contas_fixas()
        contas = [c for c in contas if c['id'] != conta_id]
        self.salvar_dados(self.contas_fixas_file, contas)
    
    def marcar_conta_como_paga(self, conta_id, mes, ano, status_pago=True, data_pagamento=None):
        """Marca uma conta fixa como paga ou pendente para um mês/ano específico"""
        contas = self.obter_contas_fixas()
        
        for conta in contas:
            if conta['id'] == conta_id:
                # Inicializando o histórico de pagamentos se não existir
                if 'historico_pagamentos' not in conta:
                    conta['historico_pagamentos'] = {}
                
                # Chave para o mês/ano no formato "MM/AAAA"
                chave_mes_ano = f"{mes:02d}/{ano}"
                
                if status_pago:
                    # Marcando como pago
                    conta['historico_pagamentos'][chave_mes_ano] = {
                        'pago': True,
                        'data_pagamento': data_pagamento or dt.now().strftime("%d/%m/%Y")
                    }
                else:
                    # Marcando como pendente (removendo do histórico)
                    if chave_mes_ano in conta['historico_pagamentos']:
                        del conta['historico_pagamentos'][chave_mes_ano]
                
                break
        
        self.salvar_dados(self.contas_fixas_file, contas)
    
    def verificar_conta_paga(self, conta_id, mes, ano):
        """Verifica se uma conta fixa está paga para um mês/ano específico"""
        contas = self.obter_contas_fixas()
        
        for conta in contas:
            if conta['id'] == conta_id:
                # Verificando se existe histórico de pagamentos
                if 'historico_pagamentos' not in conta:
                    return False
                
                # Chave para o mês/ano no formato "MM/AAAA"
                chave_mes_ano = f"{mes:02d}/{ano}"
                
                # Verificando se o mês/ano está no histórico
                return chave_mes_ano in conta['historico_pagamentos']
        
        return False
    
    def obter_data_pagamento(self, conta_id, mes, ano):
        """Obtém a data de pagamento de uma conta fixa para um mês/ano específico"""
        contas = self.obter_contas_fixas()
        
        for conta in contas:
            if conta['id'] == conta_id:
                # Verificando se existe histórico de pagamentos
                if 'historico_pagamentos' not in conta:
                    return None
                
                # Chave para o mês/ano no formato "MM/AAAA"
                chave_mes_ano = f"{mes:02d}/{ano}"
                
                # Verificando se o mês/ano está no histórico
                if chave_mes_ano in conta['historico_pagamentos']:
                    return conta['historico_pagamentos'][chave_mes_ano].get('data_pagamento')
        
        return None
    
    # Métodos para análise de dados
    def obter_gastos_por_periodo(self, mes=None, ano=None):
        """Retorna os gastos filtrados por mês e ano"""
        gastos = self.obter_gastos()
        
        if mes is not None and ano is not None:
            # Filtrando por mês e ano
            gastos_filtrados = []
            for gasto in gastos:
                data = dt.strptime(gasto['data'], "%d/%m/%Y")
                if data.month == mes and data.year == ano:
                    gastos_filtrados.append(gasto)
            return gastos_filtrados
        
        return gastos
    
    def obter_receitas_por_periodo(self, mes=None, ano=None):
        """Retorna as receitas filtradas por mês e ano"""
        receitas = self.obter_receitas()
        
        if mes is not None and ano is not None:
            # Filtrando por mês e ano
            receitas_filtradas = []
            
            for receita in receitas:
                # Verificando se é uma receita recorrente
                if receita.get('recorrente', False):
                    # Verificando se a data de início é anterior ou igual ao período solicitado
                    data_inicio = dt.strptime(receita['data_inicio'], "%d/%m/%Y")
                    
                    # Verificando se a data de fim (se existir) é posterior ou igual ao período solicitado
                    tem_data_fim = 'data_fim' in receita and receita['data_fim']
                    if tem_data_fim:
                        data_fim = dt.strptime(receita['data_fim'], "%d/%m/%Y")
                    
                    # Verificando se o período solicitado está dentro do período da receita recorrente
                    periodo_solicitado = dt(ano, mes, 1)
                    
                    if (data_inicio.year < ano or (data_inicio.year == ano and data_inicio.month <= mes)) and \
                       (not tem_data_fim or (data_fim.year > ano or (data_fim.year == ano and data_fim.month >= mes))):
                        # Criando uma cópia da receita para o período solicitado
                        receita_periodo = receita.copy()
                        receita_periodo['data'] = f"01/{mes:02d}/{ano}"
                        receitas_filtradas.append(receita_periodo)
                else:
                    # Para receitas não recorrentes, verificamos a data normalmente
                    data = dt.strptime(receita['data'], "%d/%m/%Y")
                    if data.month == mes and data.year == ano:
                        receitas_filtradas.append(receita)
            
            return receitas_filtradas
        
        return receitas
    
    def obter_contas_fixas_por_periodo(self, mes=None, ano=None):
        """Retorna as contas fixas filtradas por mês e ano"""
        contas = self.obter_contas_fixas()
        
        if mes is not None and ano is not None:
            # Filtrando por mês e ano
            contas_filtradas = []
            
            for conta in contas:
                # Verificando se a conta se aplica ao período solicitado
                if conta.get('recorrente', False):
                    # Verificando se a data de início é anterior ou igual ao período solicitado
                    data_inicio = dt.strptime(conta['data_inicio'], "%d/%m/%Y")
                    
                    # Verificando se a data de fim (se existir) é posterior ou igual ao período solicitado
                    tem_data_fim = 'data_fim' in conta and conta['data_fim']
                    if tem_data_fim:
                        data_fim = dt.strptime(conta['data_fim'], "%d/%m/%Y")
                    
                    # Verificando se o período solicitado está dentro do período da conta recorrente
                    periodo_solicitado = dt(ano, mes, 1)
                    
                    if (data_inicio.year < ano or (data_inicio.year == ano and data_inicio.month <= mes)) and \
                       (not tem_data_fim or (data_fim.year > ano or (data_fim.year == ano and data_fim.month >= mes))):
                        # Criando uma cópia da conta para o período solicitado
                        conta_periodo = conta.copy()
                        
                        # Verificando se a conta está paga para este período
                        pago = self.verificar_conta_paga(conta['id'], mes, ano)
                        data_pagamento = self.obter_data_pagamento(conta['id'], mes, ano)
                        
                        conta_periodo['pago'] = pago
                        if pago and data_pagamento:
                            conta_periodo['data_pagamento'] = data_pagamento
                        
                        # Adicionando o mês e ano para referência
                        conta_periodo['mes'] = mes
                        conta_periodo['ano'] = ano
                        
                        contas_filtradas.append(conta_periodo)
                else:
                    # Para contas não recorrentes, verificamos o mês e ano normalmente
                    if conta.get('mes') == mes and conta.get('ano') == ano:
                        contas_filtradas.append(conta)
            
            return contas_filtradas
        
        return contas
    
    def calcular_total_gastos(self, gastos=None):
        """Calcula o total de gastos"""
        if gastos is None:
            gastos = self.obter_gastos()
        
        total = 0
        for gasto in gastos:
            total += float(gasto['valor'])
        
        return total
    
    def calcular_total_receitas(self, receitas=None):
        """Calcula o total de receitas"""
        if receitas is None:
            receitas = self.obter_receitas()
        
        total = 0
        for receita in receitas:
            total += float(receita['valor'])
        
        return total
    
    def calcular_total_contas_fixas(self, contas=None):
        """Calcula o total de contas fixas"""
        if contas is None:
            contas = self.obter_contas_fixas()
        
        total = 0
        for conta in contas:
            total += float(conta['valor'])
        
        return total
    
    def calcular_saldo(self, mes=None, ano=None):
        """Calcula o saldo (receitas - gastos - contas fixas)"""
        if mes is not None and ano is not None:
            gastos = self.obter_gastos_por_periodo(mes, ano)
            receitas = self.obter_receitas_por_periodo(mes, ano)
            contas_fixas = self.obter_contas_fixas_por_periodo(mes, ano)
        else:
            gastos = self.obter_gastos()
            receitas = self.obter_receitas()
            contas_fixas = self.obter_contas_fixas()
        
        total_gastos = self.calcular_total_gastos(gastos)
        total_receitas = self.calcular_total_receitas(receitas)
        total_contas_fixas = self.calcular_total_contas_fixas(contas_fixas)
        
        return total_receitas - total_gastos - total_contas_fixas
    
    def obter_gastos_por_categoria(self, mes=None, ano=None):
        """Retorna um dicionário com os gastos agrupados por categoria"""
        if mes is not None and ano is not None:
            gastos = self.obter_gastos_por_periodo(mes, ano)
        else:
            gastos = self.obter_gastos()
        
        gastos_por_categoria = {}
        for categoria in self.categorias:
            gastos_por_categoria[categoria] = 0
        
        for gasto in gastos:
            categoria = gasto['categoria']
            valor = float(gasto['valor'])
            
            if categoria in gastos_por_categoria:
                gastos_por_categoria[categoria] += valor
            else:
                gastos_por_categoria[categoria] = valor
        
        return gastos_por_categoria
    
    def _gerar_id(self, lista):
        """Gera um ID único para um novo item"""
        if not lista:
            return 1
        
        # Encontrando o maior ID existente
        maior_id = 0
        for item in lista:
            if 'id' in item and item['id'] > maior_id:
                maior_id = item['id']
        
        # Retornando o próximo ID
        return maior_id + 1
    
    def obter_meses_anos_disponiveis(self):
        """Retorna uma lista de tuplas (mes, ano) disponíveis nos dados"""
        gastos = self.obter_gastos()
        receitas = self.obter_receitas()
        contas_fixas = self.obter_contas_fixas()
        
        meses_anos = set()
        
        # Adicionando meses/anos dos gastos
        for gasto in gastos:
            data = dt.strptime(gasto['data'], "%d/%m/%Y")
            meses_anos.add((data.month, data.year))
        
        # Adicionando meses/anos das receitas
        for receita in receitas:
            if receita.get('recorrente', False):
                # Para receitas recorrentes, adicionamos todos os meses entre a data de início e fim
                data_inicio = dt.strptime(receita['data_inicio'], "%d/%m/%Y")
                
                # Se tiver data de fim, usamos ela, senão usamos a data atual
                if 'data_fim' in receita and receita['data_fim']:
                    data_fim = dt.strptime(receita['data_fim'], "%d/%m/%Y")
                else:
                    data_fim = dt.now()
                
                # Adicionando todos os meses entre data_inicio e data_fim
                data_atual = data_inicio
                while data_atual <= data_fim:
                    meses_anos.add((data_atual.month, data_atual.year))
                    
                    # Avançando para o próximo mês
                    if data_atual.month == 12:
                        data_atual = dt(data_atual.year + 1, 1, 1)
                    else:
                        data_atual = dt(data_atual.year, data_atual.month + 1, 1)
            else:
                # Para receitas não recorrentes, adicionamos apenas o mês/ano da data
                data = dt.strptime(receita['data'], "%d/%m/%Y")
                meses_anos.add((data.month, data.year))
        
        # Adicionando meses/anos das contas fixas
        for conta in contas_fixas:
            if conta.get('recorrente', False):
                # Para contas recorrentes, adicionamos todos os meses entre a data de início e fim
                data_inicio = dt.strptime(conta['data_inicio'], "%d/%m/%Y")
                
                # Se tiver data de fim, usamos ela, senão usamos a data atual
                if 'data_fim' in conta and conta['data_fim']:
                    data_fim = dt.strptime(conta['data_fim'], "%d/%m/%Y")
                else:
                    data_fim = dt.now()
                
                # Adicionando todos os meses entre data_inicio e data_fim
                data_atual = data_inicio
                while data_atual <= data_fim:
                    meses_anos.add((data_atual.month, data_atual.year))
                    
                    # Avançando para o próximo mês
                    if data_atual.month == 12:
                        data_atual = dt(data_atual.year + 1, 1, 1)
                    else:
                        data_atual = dt(data_atual.year, data_atual.month + 1, 1)
            else:
                # Para contas não recorrentes, adicionamos apenas o mês/ano especificado
                meses_anos.add((conta['mes'], conta['ano']))
        
        # Ordenando por ano e mês
        return sorted(list(meses_anos), key=lambda x: (x[1], x[0]))
    
    def obter_dados_para_historico(self, mes, ano):
        """Retorna todos os dados (gastos, receitas, contas fixas) para um determinado mês/ano"""
        gastos = self.obter_gastos_por_periodo(mes, ano)
        receitas = self.obter_receitas_por_periodo(mes, ano)
        contas_fixas = self.obter_contas_fixas_por_periodo(mes, ano)
        
        # Preparando os dados para exibição
        dados_historico = []
        
        # Adicionando gastos
        for gasto in gastos:
            dados_historico.append({
                'tipo': 'Gasto',
                'descricao': gasto['descricao'],
                'categoria': gasto['categoria'],
                'valor': gasto['valor'],
                'data': gasto['data'],
                'status': '-'
            })
        
        # Adicionando receitas
        for receita in receitas:
            recorrente = receita.get('recorrente', False)
            status = 'Recorrente' if recorrente else '-'
            
            dados_historico.append({
                'tipo': 'Receita',
                'descricao': receita['descricao'],
                'categoria': 'Receita',
                'valor': receita['valor'],
                'data': receita.get('data', f"01/{mes:02d}/{ano}"),
                'status': status
            })
        
        # Adicionando contas fixas
        for conta in contas_fixas:
            status = 'Pago' if conta.get('pago', False) else 'Pendente'
            recorrente = conta.get('recorrente', False)
            if recorrente:
                status += ' (Recorrente)'
                
            data = conta.get('data_pagamento', f"01/{mes:02d}/{ano}")
            
            # Verificando se é uma conta parcelada
            parcelado = conta.get('parcelado', False)
            
            # Criando um dicionário com os dados da conta
            conta_historico = {
                'tipo': 'Conta Fixa',
                'descricao': conta['descricao'],
                'categoria': 'Conta Fixa',
                'valor': conta['valor'],
                'data': data,
                'status': status
            }
            
            # Adicionando informações de parcelamento se aplicável
            if parcelado:
                conta_historico['parcelado'] = True
                conta_historico['num_parcelas'] = conta.get('num_parcelas', 1)
                
                # Adicionando data de início para cálculo da parcela atual
                if 'data_inicio' in conta:
                    conta_historico['data_inicio'] = conta['data_inicio']
                
                # Adicionando informação de juros, se existir
                if 'valor_com_juros' in conta and conta['valor_com_juros']:
                    conta_historico['valor_com_juros'] = conta['valor_com_juros']
                    # O valor original é o valor sem juros
                    conta_historico['valor_sem_juros'] = conta['valor']
            
            dados_historico.append(conta_historico)
        
        # Ordenando por data
        return sorted(dados_historico, key=lambda x: dt.strptime(x['data'], "%d/%m/%Y") if isinstance(x['data'], str) else x['data'])
