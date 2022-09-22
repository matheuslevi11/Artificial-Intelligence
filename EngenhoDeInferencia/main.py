import pandas as pd
import re
from utils import importKnowledgeBase, read_question, scan

def parse_rule(rule):
    rule = rule.split(' ')
    for i in range(len(rule)):
        e = rule[i]
        if e != 'and' and e != 'or':
            rule[i] = infer(e)
    return rule

def evaluate_expressions(exps):
    while len(exps) > 1:
        for i in range(len(exps)):
            if exps[i] == 'and':
                if exps[i-1] and exps[i+1]:
                    exps[i] = True
                else:
                    exps[i] = False
                
                del exps[i+1]
                del exps[i-1]
                break
            elif exps[i] == 'or':
                if exps[i-1] or exps[i+1]:
                    exps[i] = True
                else:
                    exps[i] = False
                
                del exps[i+1]
                del exps[i-1]
                break
    
    return exps[0]
            
def infer(goal):
    global base_fatos, base_regras

    if goal in base_fatos.FATO.to_list():
        value = base_fatos[base_fatos.FATO == goal].values[0][1]
        return value

    for i, r in base_regras.iterrows():
        if goal == r['CONSEQUENTE']:
            expressions = parse_rule(r['ANTECEDENTE'])
            return evaluate_expressions(expressions)
    
    print(f'Não consigo inferir {goal}')
    
    # Pergunta ao usuário já que o fato não pode ser inferido e salva na memória de trabalho
    value = input(f'Valor de {goal} (V/F): ').upper()
    value = 'True' if value == 'V' else 'False'
    base_fatos.loc[len(base_fatos.index)] = [goal, value]
    
    return True if value == 'True' else False

if __name__ == '__main__':
    print('Bem vindo a Máquina de Inferência')
    print('Para alimentar a base de conhecimento, adicione os dados nos arquivos da pasta BaseDeConhecimento')
    print('Foram detectados os seguintes fatos:', end=' ')
    fatos = scan()
    for fato in fatos:
        print(fato, end=' ')
    print()

    q = read_question(fatos)
    global base_fatos, base_regras
    base_fatos, base_regras = importKnowledgeBase()
    answer = infer(q)
    print(f'A resposta é: {answer}')