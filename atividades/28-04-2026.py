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
    home_scores: List[int]
    away_scores: List[int]


class InsightCalculadoEngine:
    def __init__(self, data: Dict[str, Any]):
        self.raw = data
        self.prepared = self._prepare_data(data)

    # --------------------------------------------------------
    # Preparação
    # --------------------------------------------------------
    def _prepare_data(self, data: Dict[str, Any]) -> PreparedData:
        dados = data.get("dados", [])

        home_scores = []
        away_scores = []

        for item in dados:
            h = to_float(item.get("homeScore"))
            a = to_float(item.get("awayScore"))

            if h is not None:
                home_scores.append(int(h))
            if a is not None:
                away_scores.append(int(a))

        return PreparedData(
            home_scores=home_scores,
            away_scores=away_scores
        )

    # --------------------------------------------------------
    # Aula 2 (estatística)
    # --------------------------------------------------------
    def aula_2(self) -> Dict[str, Any]:

        def resumo(values: List[float]) -> Dict[str, Optional[float]]:
            return {
                "media": round_or_none(safe_mean(values), 4),
                "mediana": round_or_none(safe_median(values), 4),
                "moda": round_or_none(safe_mode(values), 4),
                "amplitude": round_or_none(amplitude(values), 4),
                "variancia": round_or_none(safe_variance(values), 4),
                "desvio_padrao": round_or_none(safe_std(values), 4),
                "minimo": round_or_none(safe_min(values), 4),
                "maximo": round_or_none(safe_max(values), 4),
            }

        return {
            "calculos": {
                "home_scores": resumo(self.prepared.home_scores),
                "away_scores": resumo(self.prepared.away_scores),
            },
            "insights": [
                "A média indica o desempenho médio dos times.",
                "A variância mostra o quanto os placares variam entre os jogos.",
                "Diferenças grandes podem indicar inconsistência ou jogos atípicos.",
            ],
        }



engine = InsightCalculadoEngine({})

# teste com aula 2

dados_empresa = load_json("atividades\Games.json")
engine = InsightCalculadoEngine(dados_empresa)
resultado = engine.aula_2()
print(resultado)