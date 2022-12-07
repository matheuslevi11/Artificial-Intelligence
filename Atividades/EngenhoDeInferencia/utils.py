import pandas as pd
import re
from style import *

def importKnowledgeBase(facts="fatos", rules="regras"):
    base_fatos = pd.read_csv(f'BaseDeConhecimento/{facts}.csv')
    base_regras = pd.read_csv(f'BaseDeConhecimento/{rules}.csv')
    return base_fatos, base_regras

def scan():
    fatos = []
    base_fatos, base_regras = importKnowledgeBase()
    
    for f in base_fatos.FATO:
        fatos.append(f)
    
    for f in base_regras.CONSEQUENTE:
        if f not in fatos:
            fatos.append(f)
    
    for r in base_regras.ANTECEDENTE:
        for f in re.findall('[A-Z]*', r):
            if f not in fatos and f != '':
                fatos.append(f)
    return fatos

def show_rules():
    base_fatos, base_regras = importKnowledgeBase()

    for i, data in base_regras.iterrows():
        print_lpurple(f"Se {data['ANTECEDENTE']} Então é {data['CONSEQUENTE']}")

def get_rule(r):
    return f"Se {r['ANTECEDENTE']} Então é {r['CONSEQUENTE']}"

def read_question(fatos):
    while True:
        q = input('Faça uma pergunta: ').upper()
        if q in fatos:
            return q
        else:
            print('Você precisa digitar uma proposição existente!')
