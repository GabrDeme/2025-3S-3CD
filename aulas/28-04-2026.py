import json
import math
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple


# ============================================================
# Funções auxiliares
# ============================================================


# Esse código define uma função simples em Python para ler e carregar um arquivo JSON
# O parâmetro path: str indica que a função espera receber o caminho do arquivo como uma string.
# -> Dict[str, Any] é uma type hint (anotação de tipo), sugerindo que a função retorna um dicionário
# com chaves do tipo str e valores de qualquer tipo (Any).
def load_json(path: str) -> Dict[str, Any]:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

# Esse código é o complemento natural do anterior: enquanto load_json lê um JSON,
# essa função salva dados em formato JSON em um arquivo.
def save_json(path: str, data: Dict[str, Any]) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
# path: str: caminho onde o arquivo será salvo.
# data: Dict[str, Any]: os dados que serão gravados (normalmente um dicionário).
# -> None: indica que a função não retorna nada (apenas executa a escrita).
# json.dump() converte o objeto Python (data) para JSON e escreve no arquivo f.
# ensure_ascii=False: permite que caracteres como á, ç, ã sejam gravados normalmente (sem virar códigos Unicode tipo \u00e1).
# indent=2: formata o JSON com indentação de 2 espaços, deixando o arquivo mais legível (bom para humanos).

# Essa função é um pequeno “conversor inteligente” que tenta transformar diferentes tipos de entrada em float,
# lidando especialmente com valores monetários no formato brasileiro.
def to_float(value: Any) -> Optional[float]:
# value: Any: aceita qualquer tipo de valor.
# -> Optional[float]: pode retornar um float ou None (caso não consiga converter).
    if value is None or value == "":
        return None
    if isinstance(value, (int, float)):  # Se já for número (int ou float), apenas converte para float (padroniza o tipo).
        return float(value)
    if isinstance(value, str):           # Se for string, entra no processamento mais interessante
        clean = value.strip().replace("R$", "").replace(".", "").replace(",", ".")
        try:
            return float(clean)
        except ValueError:
            return None
    return None
# strip(): remove espaços no começo e fim.
# replace("R$", ""): remove símbolo de moeda brasileira.
# replace(".", ""): remove separador de milhar.
# replace(",", "."): troca vírgula por ponto (formato decimal padrão do Python).


# Recebe qualquer tipo (Any).
# Retorna True, False ou None.
def to_bool(value: Any) -> Optional[bool]:
    if value is None or value == "":
        return None
    if isinstance(value, bool):  # Se já for booleano (True ou False), retorna direto.
        return value
    # Converte números: 0 → False, qualquer outro número → True
    if isinstance(value, (int, float)):  
        return bool(value)
    if isinstance(value, str):         # Se for string: remove espaços (strip) e converte para minúsculas (lower)
        text = value.strip().lower()
        if text in {"true", "1", "sim", "s", "yes", "y"}:
            return True
        if text in {"false", "0", "nao", "não", "n", "no"}:
            return False
        # Isso facilita comparar valores como "Sim", " SIM " etc.
    return None


# Essa função tenta interpretar uma data em diferentes formatos e padronizá-la para o formato ISO "YYYY-MM-DD".
# Se não conseguir converter, ela devolve o valor original (no caso de string) ou None.
def parse_date(value: Any) -> Optional[str]:
# Recebe qualquer tipo (Any).
# Retorna uma str (data formatada) ou None.
    if value is None or value == "":
        return None
    if isinstance(value, str):  # Só tenta converter se o valor for uma string.
        for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d", "%d-%m-%Y"):
            # Define uma lista de formatos aceitos:
            # "2025-04-25" (ISO)
            # "25/04/2025" (brasileiro comum)
            # "2025/04/25"
            # "25-04-2025"
            try:
                return datetime.strptime(value, fmt).strftime("%Y-%m-%d")
            # strptime converte uma string em um objeto de data
            # fmt define como a string está formatada
            # strftime converte o objeto de volta para string em um formato específico
            except ValueError:
                continue
        return value
    return None
# Tenta:
# Interpretar a string como data usando strptime.
# Se der certo, formata com strftime para "YYYY-MM-DD" (padrão ISO).
# Assim, independente do formato de entrada, a saída fica consistente.


# Essa função é uma forma segura e concisa de calcular a média de uma lista de números, evitando erro quando a lista está vazia.
def safe_mean(values: List[float]) -> Optional[float]:
# Recebe uma lista de números (List[float]).
# Retorna um float (a média) ou None se não houver dados.
    return statistics.mean(values) if values else None
# Usa uma expressão condicional (forma curta de if).
# if values: em Python, listas vazias são avaliadas como False.
# Se a lista tem elementos → calcula statistics.mean(values)
# Se a lista está vazia → retorna None

# Essa função segue exatamente a mesma ideia da safe_mean, mas para mediana: ela calcula o valor central
# de uma lista de números de forma segura, evitando erro quando a lista está vazia.
def safe_median(values: List[float]) -> Optional[float]:
    return statistics.median(values) if values else None

# Essa função calcula a moda (o valor mais frequente) de forma segura e um pouco
# mais flexível que statistics.mode, evitando exceções e lidando com empates.
def safe_mode(values: List[float]) -> Optional[float]:
    if not values:   # Se a lista estiver vazia, retorna None.
        return None
    counts = Counter(values)          # Usa Counter (da biblioteca collections) para contar quantas vezes cada valor aparece.
    top_count = max(counts.values())  # Encontra a maior frequência (quantas vezes o valor mais comum aparece).
    # Cria uma lista com todos os valores que têm essa frequência máxima.
    # Isso resolve o problema de múltiplas modas.
    top_values = [k for k, v in counts.items() if v == top_count]
    return top_values[0] if top_values else None   # se der empate, retorna apenas o primeiro valor da lista
# Retorna o primeiro valor da lista de modas.
# Se por algum motivo estiver vazia (improvável aqui), retorna None.
# Exemplo:
# counts = {1: 2, 2: 2, 3: 1}
# Isso significa:
# número 1 aparece 2 vezes
# número 2 aparece 2 vezes
# número 3 aparece 1 vez
# Você está dizendo:

# k = número (a chave)
# v = quantidade (o valor)

# Então isso roda assim:

# k	v
# 1	2
# 2	2
# 3	1

# Forma longa:

# top_values = []

#for k, v in counts.items():
#    if v == top_count:
#        top_values.append(k)

#Tradução:

#olha cada número (k)
#se a quantidade (v) for a maior
#guarda esse número

def safe_variance(values: List[float]) -> Optional[float]:
    return statistics.variance(values) if len(values) > 1 else 0.0 if values else None
# if values testa se a variável esta vazia ou se tem valores

# forma alternativa
#def safe_variance(values: List[float]) -> Optional[float]:
#    if not values:
#        return None
#    if len(values) == 1:
#        return 0.0
#    return statistics.variance(values)

# idem anterior, porem calcula o desvio padrão
def safe_std(values: List[float]) -> Optional[float]:
    return statistics.stdev(values) if len(values) > 1 else 0.0 if values else None

# retorna mínimo
def safe_min(values: List[float]) -> Optional[float]:
    return min(values) if values else None

# retorna máximo
def safe_max(values: List[float]) -> Optional[float]:
    return max(values) if values else None

# retorna a amplitude
def amplitude(values: List[float]) -> Optional[float]:
    return (max(values) - min(values)) if values else None

# Essa função gera um relatório de valores nulos (ou vazios) em uma lista de registros
# (dicionários). Ela conta quantos campos estão “faltando” em cada chave.
def null_report(records: List[Dict[str, Any]]) -> Dict[str, int]:
    # Função que conta valores nulos ou vazios em cada campo
    # records = lista de dicionários (tipo linhas de uma tabela)
    # retorna um dicionário com contagem de nulos por coluna
    counts: Dict[str, int] = Counter()  # counts deve se comportar como dicionário com chaves do tipo str e valores do tipo int
    # Counter é um tipo especial de dicionário usado para contar ocorrências.
    # Cria um contador vazio para armazenar quantos nulos cada chave tem
    for rec in records:   # Percorre cada registro (cada "linha" de dados)
        for k, v in rec.items():  # Percorre cada campo (chave e valor) dentro do registro
            # k recebe a chave (key)
            # v recebe o valor (value) associado a essa chave
            if v is None or v == "":  # Verifica se o valor está vazio (None ou string vazia)
                counts[k] += 1    # Incrementa 1 na contagem daquela chave
    return dict(counts)   # Converte o Counter para dict normal e retorna
# dict(counts) pega o objeto counts (que no seu caso é um Counter) e converte para um dicionário comum (dict).



# Essa função tenta inferir automaticamente o tipo de um campo de dados, ou seja,
# ela olha para uma lista de valores e decide se aquilo parece número, categoria, texto etc.
# Isso é muito usado em análise de dados e sistemas que “auto-entendem” tabelas.
def infer_field_type(values: List[Any]) -> str:
    # Função que tenta descobrir o tipo de uma coluna de dados
    not_null = [v for v in values if v is not None and v != ""] # Remove valores vazios (None ou "")
    if not not_null:          # Se não sobrou nenhum valor válido
        return "indefinido"
    # Conta quantos valores podem ser interpretados como números
    # (diretamente ou via conversão com to_float)
    numeric = sum(1 for v in not_null if isinstance(v, (int, float)) or to_float(v) is not None)
    if numeric == len(not_null):  # Se TODOS os valores são numéricos
        unique = len(set(float(to_float(v)) for v in not_null if to_float(v) is not None)) # Conta quantos valores numéricos diferentes existem
        # Um set guarda apenas valores únicos (remove duplicatas)
        if unique <= 12:   # Poucos valores distintos → provavelmente discreto
            return "quantitativa_discreta"
        return "quantitativa_continua"  # Muitos valores distintos → contínuo (ex: salário, peso)
    unique = len(set(str(v) for v in not_null))  # Se não for totalmente numérico, trata como texto e conta categorias únicas
    if unique <= 12:  # Poucas categorias → variável categórica simples
        return "qualitativa_nominal"
    return "qualitativa_ordinal_ou_textual"  # Muitas categorias → texto livre ou variável ordenada complexa

# mesmo código escrito de outra forma
# not_null = []
# for v in values:
#     if v is not None and v != "":
#        not_null.append(v)




# Essa função serve para arredondar números com segurança, sem quebrar o código quando o valor não for numérico.
def round_or_none(value: Optional[float], ndigits: int = 4) -> Optional[float]:
    # Função que arredonda um número, se ele for válido
    # Caso contrário, retorna o próprio valor (geralmente None)
    return round(value, ndigits) if isinstance(value, (int, float)) else value
    # Se value for int ou float → arredonda
    # Senão (ex: None, string) → retorna como está


# Essa função aplica arredondamento em toda uma lista de valores, usando a função round_or_none que você viu antes.
def round_list(values: List[Optional[float]], ndigits: int = 4) -> List[Optional[float]]:
    # Função que arredonda todos os elementos de uma lista
    # Mantém None ou valores não numéricos intactos
    return [round_or_none(v, ndigits) for v in values]
    # Para cada valor v na lista:
    # → aplica round_or_none
    # → retorna nova lista com valores arredondados






# Esse código define uma classe chamada PreparedData, mas na forma atual ela está sendo usada como um
# “container de dados” (data structure) — ou seja, não tem lógica, só organiza informações.
# @dataclass é um decorador do Python (do módulo dataclasses) que serve para criar classes focadas em armazenar
# dados sem precisar escrever muito código repetitivo.
# Um decorador em Python é uma forma de modificar ou estender o comportamento
# de uma função ou classe sem alterar o código original dela.
# Ele é basicamente uma função que “envolve” outra função.

@dataclass
class PreparedData:
    negocio: Dict[str, Any]
    transacoes: List[Dict[str, Any]]
    dias: List[Dict[str, Any]]
    recepcao: Dict[str, Any]

# Esse trecho define uma classe chamada InsightCalculadoEngine, que é o
# “motor” responsável por processar dados e gerar insights.
class InsightCalculadoEngine:
    def __init__(self, data: Dict[str, Any]):
        # self representa a própria instância do objeto que está sendo criada ou usada
        self.raw = data                            # guarda os dados originais
        self.prepared = self._prepare_data(data)   # chama o método da própria classe e salva o resultado em prepared

    # --------------------------------------------------------
    # Preparação
    # --------------------------------------------------------
    # Esse método _prepare_data é o coração do processamento de dados da sua classe. Ele pega
    # dados brutos e transforma em um formato limpo, padronizado e pronto para análise.
    def _prepare_data(self, data: Dict[str, Any]) -> PreparedData:
        negocio = data.get("negocio", {})
        dados = data.get("dados", {})
        recepcao = data.get("recepcao", {})
        # dict.get(chave, valor_padrao):
        # retorna o valor da chave se ela existir
        # se não existir, retorna o valor_padrao (em vez de dar erro)
        # se não existir, retorna {} (dicionário vazio)

        transacoes = []   # criando lista vazia
        for item in dados.get("transacoes",[]):     # [] retorna uma lista vazia
            record = dict(item)                     # cria um dicionário (dict) a partir de item.
            record["data"] = parse_date(record.get("data"))  # trata o formato de data
            if "valor" in record:
                record["valor"] = to_float(record.get("valor"))     # trata float
            if "pago_no_prazo" in record:
                record["pago_no_prazo"] = to_bool(record.get("pago_no_prazo"))   # trata boolean
            if "desconto" in record:
                record["desconto"] = to_float(record.get("desconto"))    # trata float
            if "marketing" in record:
                record["marketing"] = to_float(record.get("marketing"))  # trata float
            transacoes.append(record)     # adicionando na lista

        dias = []    # criando lista vazia
        for item in dados.get("dias", []):
            record = dict(item)
            record["data"] = parse_date(record.get("data"))
            for field in ["receita", "despesa", "vendas_qtd", "clientes", "marketing", "desconto_medio"]:
                if field in record:  # verifica se a chave field existe dentro do dicionário record
                    record[field] = to_float(record.get(field))   # trata float
            dias.append(record)

        if not dias and transacoes:
            dias = self._derive_daily_records(transacoes)

        return PreparedData(negocio=negocio, transacoes=transacoes, dias=dias, recepcao=recepcao)

#Esse método _derive_daily_records é uma agregação de transações por dia. Ele pega dados “linha a linha” (transações) e
#transforma em um resumo diário estruturado — tipo o que você veria em um dashboard.
    def _derive_daily_records(self, transacoes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        by_day: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            "receita": 0.0,
            "despesa": 0.0,
            "vendas_qtd": 0,
            "clientes": set(),
            "marketing": 0.0,
            "desconto_medio_soma": 0.0,
            "desconto_medio_qtd": 0,
            "transacoes_qtd": 0,
        })

        for t in transacoes:
            day = t.get("data") or "sem_data"
            info = by_day[day]
            info["transacoes_qtd"] += 1
            valor = t.get("valor") or 0.0
            tipo = str(t.get("tipo", "")).lower()
            if tipo == "receita":
                info["receita"] += valor
                info["vendas_qtd"] += 1
            elif tipo == "despesa":
                info["despesa"] += valor
            info["marketing"] += (t.get("marketing") or 0.0)
            desconto = t.get("desconto")
            if desconto is not None:
                info["desconto_medio_soma"] += desconto
                info["desconto_medio_qtd"] += 1
            cliente = t.get("cliente")
            if cliente:
                info["clientes"].add(str(cliente))

        daily_records = []
        for day, info in sorted(by_day.items(), key=lambda x: x[0]):
            qtd_desc = info["desconto_medio_qtd"]
            daily_records.append({
                "data": day,
                "receita": round(info["receita"], 2),
                "despesa": round(info["despesa"], 2),
                "vendas_qtd": int(info["vendas_qtd"]),
                "clientes": int(len(info["clientes"])),
                "marketing": round(info["marketing"], 2),
                "desconto_medio": round((info["desconto_medio_soma"] / qtd_desc), 4) if qtd_desc else 0.0,
                "transacoes_qtd": int(info["transacoes_qtd"]),
            })
        return daily_records

    # --------------------------------------------------------
    # Séries auxiliares
    # --------------------------------------------------------

# Esse método _series_from_days transforma os dados diários em séries numéricas separadas, ou seja,
# ele reorganiza o dataset para ficar pronto para análises estatísticas e gráficos (ou machine learning).
    
    def _series_from_days(self) -> Dict[str, List[float]]:
        dias = self.prepared.dias  # Obtém a lista de dias já preparados (provavelmente um array de dicionários com métricas diárias)
        receita = [d.get("receita") for d in dias if d.get("receita") is not None]
        # Cria uma lista com os valores de receita de cada dia
        # Ignora dias onde "receita" é None
        despesa = [d.get("despesa") for d in dias if d.get("despesa") is not None]
        # Cria uma lista com os valores de despesa
        # Também ignora valores None
        lucro = []        # Inicializa a lista de lucro (será calculada manualmente)
        for d in dias:    # Itera sobre cada dia
            if d.get("receita") is not None and d.get("despesa") is not None:
                lucro.append(float(d["receita"]) - float(d["despesa"])) # Só calcula lucro se ambos os valores existirem
        vendas_qtd = [int(d.get("vendas_qtd") or 0) for d in dias]
        # Cria lista com quantidade de vendas por dia
        # Se não existir valor, usa 0
        # Converte tudo para inteiro
        clientes = [float(d.get("clientes") or 0) for d in dias]
        # Lista com número de clientes por dia
        # Usa 0 como padrão e converte para float
        marketing = [float(d.get("marketing") or 0) for d in dias]
        # Lista com valores de investimento em marketing
        # Também garante float e valor padrão 0
        desconto_medio = [float(d.get("desconto_medio") or 0) for d in dias]
        # Lista com desconto médio aplicado por dia
        # Usa 0 se não houver valor
        transacoes_qtd = [int(d.get("transacoes_qtd") or d.get("vendas_qtd") or 0) for d in dias]
        # Lista com quantidade de transações
        # Prioridade:
        # 1. "transacoes_qtd"
        # 2. "vendas_qtd" (fallback)
        # 3. 0 (se nenhum existir)
        return {                           # Retorna um dicionário contendo todas as séries organizadas por tipo
            "receita": receita,
            "despesa": despesa,
            "lucro": lucro,
            "vendas_qtd": vendas_qtd,
            "clientes": clientes,
            "marketing": marketing,
            "desconto_medio": desconto_medio,
            "transacoes_qtd": transacoes_qtd,
        }

# Esse método _ticket_values extrai uma lista de valores de “tickets” (valores de vendas) a partir
#das transações — mais especificamente, ele pega somente as receitas.
    def _ticket_values(self) -> List[float]:
        tickets = []  # Inicializa uma lista vazia que armazenará os valores dos tickets (receitas)
        for t in self.prepared.transacoes:   # Percorre cada transação presente na estrutura preparada
            if str(t.get("tipo", "")).lower() == "receita" and t.get("valor") is not None:
                 # Verifica duas condições:
                 # 1. O tipo da transação é "receita" (case insensitive)
                 # - usa .get("tipo", "") para evitar erro se a chave não existir
                 # - converte para string e minúsculo para padronizar comparação
                 # 2. O campo "valor" não é None (garante que existe um valor válido)
                tickets.append(float(t["valor"]))  # Converte o valor da transação para float e adiciona à lista
        return tickets  # Retorna a lista contendo todos os valores de tickets encontrados

    # --------------------------------------------------------
    # Aulas
    # --------------------------------------------------------

    # Esse método aula_1 é basicamente uma função de “análise exploratória inicial” (EDA) do seu sistema.
    # Ele organiza informações básicas do dataset para responder: “o que eu tenho de dados aqui?”
    def aula_1(self) -> Dict[str, Any]:   # Define o método "aula_1", que retorna um dicionário com análises iniciais dos dados
        transacoes = self.prepared.transacoes   # Extrai a lista de transações já preparadas
        dias = self.prepared.dias               # Extrai a lista de registros diários já preparados
        if transacoes:                          # Verifica se existem transações
            keys = sorted({k for rec in transacoes for k in rec.keys()})      # sorted transforma o set em uma lista ordenada
            # Cria um conjunto com todas as chaves existentes nas transações
            # Depois converte em lista ordenada
            # Ex: ["valor", "data", "tipo", "cliente"]
            classificacao = {}    # Inicializa dicionário que armazenará o tipo de cada campo
            for key in keys:      # Itera sobre cada campo existente nas transações
                valores = [rec.get(key) for rec in transacoes]   # Coleta todos os valores daquele campo em todas as transações
                classificacao[key] = infer_field_type(valores)
                # Usa uma função que infere o tipo do campo
                # Ex: quantitativa, qualitativa, etc.
        else:   # Caso não existam transações
            classificacao = {}    # Define classificação vazia

        sample_size = min(5, len(transacoes))   # Define tamanho da amostra (no máximo 5 registros)
        amostra = transacoes[:sample_size]      # Pega os primeiros registros como amostra

        return {  # Retorna um relatório estruturado com análises da "aula 1"
            "tema": "Entender os dados do negócio",  # Define o objetivo da análise
            # Descreve o problema de negócio em linguagem simples
            "problema_financeiro": "O empreendedor possui dados, mas não sabe o que está registrando nem como organizar isso para análise.",
            "calculos": {  # Seção com métricas e cálculos
                "populacao_transacoes": len(transacoes),    # Quantidade total de transações
                "populacao_registros_diarios": len(dias),   # Quantidade total de registros diários
                "amostra_exibida": sample_size,             # Quantidade de registros mostrados na amostra
                "classificacao_campos_transacoes": classificacao,        # Tipos de cada campo das transações
                "campos_faltantes_transacoes": null_report(transacoes),  # Conta valores nulos/vazios nas transações
                "campos_faltantes_dias": null_report(dias),  # Conta valores nulos/vazios nos dados diários
                "amostra_transacoes": amostra,               # Exibe amostra dos dados
            },
            "insights": [ # Lista de interpretações automáticas
                # Explica o objetivo da análise de tipos
                "Nesta etapa o sistema identifica quais campos são qualitativos e quais são quantitativos.",
                # Explica que o sistema detecta problemas nos dados
                "Também aponta lacunas iniciais para preparar a análise exploratória das próximas aulas.",
            ],
        }

    def aula_2(self) -> Dict[str, Any]:    # Define o método aula_2,
        #que retorna um relatório estatístico do negócio

        # Converte os dados diários em séries numéricas (listas)
        # Ex: receita = [100, 200, 150, ...]

        series = self._series_from_days()
        tickets = self._ticket_values()     # Extrai valores de vendas (receitas) para análise de ticket

        def resumo(values: List[float]) -> Dict[str, Optional[float]]:  # Função interna que calcula estatísticas descritivas de uma lista
            return {
                "media": round_or_none(safe_mean(values), 4),       # Calcula a média dos valores e arredonda
                "mediana": round_or_none(safe_median(values), 4),   # Calcula a mediana (valor central) 
                "moda": round_or_none(safe_mode(values), 4),        # Calcula a moda (valor mais frequente)
                "amplitude": round_or_none(amplitude(values), 4),   # Diferença entre máximo e mínimo
                "variancia": round_or_none(safe_variance(values), 4),  # Mede dispersão dos dados
                "desvio_padrao": round_or_none(safe_std(values), 4),   # Mede o quanto os valores variam em torno da média
                "minimo": round_or_none(safe_min(values), 4),       # Menor valor da lista
                "maximo": round_or_none(safe_max(values), 4),       # Maior valor da lista
            }

        return {# Retorna um relatório estruturado da aula 2
            "tema": "Descobrir o comportamento financeiro central do negócio",  # Define o objetivo da análise
            # Explica o problema de negócio
            "problema_financeiro": "O empreendedor não sabe qual é o comportamento financeiro típico do negócio.",
            "calculos": { # Bloco com cálculos estatísticos principais
                "receita_diaria": resumo(series["receita"]),   # Estatísticas da receita por dia
                "despesa_diaria": resumo(series["despesa"]),   # Estatísticas da despesa por dia
                "lucro_diario": resumo(series["lucro"]),       # Estatísticas do lucro por dia
                "ticket_receita": resumo(tickets),             # Estatísticas dos valores de venda (ticket médio)
            },
            "insights": [  # Interpretações automáticas dos dados
                # Explica diferença entre medidas de tendência central
                "A média mostra o comportamento central, enquanto mediana e moda ajudam a validar se há distorções.",
                # Explica dispersão e estabilidade do negócio
                "A variância e o desvio padrão ajudam a medir estabilidade financeira.",
            ],
        }



engine = InsightCalculadoEngine({})

# teste com aula 2

dados_empresa = load_json("aulas\exemplo_entrada_insight_calculado.json")
engine = InsightCalculadoEngine(dados_empresa)
resultado = engine.aula_2()             
print("\nTeste 2 - aula2")
print(resultado)
save_json("teste_saida_aula2b.json", resultado)

#print("Media1="+str(safe_mean([0,0,0,0,0,10,10,10,10,10])))
#print("Variancia1="+str(safe_variance([0,0,0,0,0,10,10,10,10,10])))
#print("Media2="+str(safe_mean([4.5,4.5,4.5,4.5,4.5,5.5,5.5,5.5,5.5,5.5])))
#print("Variancia2="+str(safe_variance([4.5,4.5,4.5,4.5,4.5,5.5,5.5,5.5,5.5,5.5])))

#print(amplitude([-1,1,2,2,2,3,4,5]))

    


    



















    
    
    
    

    


