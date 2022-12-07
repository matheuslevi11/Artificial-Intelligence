from utils import *
from style import *

def parse_rule_forward(rule):
    rule = rule.split(' ')
    for i in range(len(rule)):
        e = rule[i]
        if e != 'and' and e != 'or':
            if e in base_fatos.FATO.to_list():
                value = base_fatos[base_fatos.FATO == e].values[0][1]
                rule[i] = value
            else:
                rule[i] = False
    return rule

def parse_rule(rule):
    rule = rule.split(' ')
    for i in range(len(rule)):
        e = rule[i]
        if e != 'and' and e != 'or':    
            rule[i] = infer_backwards(e)
            if '!' in e:
                rule[i] = not rule[i]
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
            
def infer_backwards(goal):
    global base_fatos, base_regras, explanation

    if goal in base_fatos.FATO.to_list():
        value = base_fatos[base_fatos.FATO == goal].values[0][1]
        explanation.append(goal)
        return value

    for i, r in base_regras.iterrows():
        if goal == r['CONSEQUENTE']:
            expressions = parse_rule(r['ANTECEDENTE'])
            value = evaluate_expressions(expressions)
            if value:
                explanation.append(get_rule(r))
            return value
    
    print(f'O animal possui esta característica? {goal}')
    
    # Pergunta ao usuário já que o fato não pode ser inferido e salva na memória de trabalho
    value = input(f'{goal} (V/F): ').upper()
    value = 'True' if value == 'V' else 'False'
    base_fatos.loc[len(base_fatos.index)] = [goal, value]
    
    return True if value == 'True' else False

def infer_forwards():
    global base_fatos, base_regras
    rules_to_apply = [-1]
    
    while len(rules_to_apply) > 0:
        rules_to_apply = []
        for i, r in base_regras.iterrows():
            exp = parse_rule_forward(r['ANTECEDENTE'])
            antecedent = evaluate_expressions(exp)
            consequent = r['CONSEQUENTE']
            if antecedent and consequent not in base_fatos.FATO.to_list():
                rules_to_apply.append(consequent)
        
        for rule in rules_to_apply:
            print(f'Foi descoberto que {rule} é verdade.')
            base_fatos.loc[len(base_fatos.index)] = [rule, 'True']

def infer_mixed():
    global base_fatos, base_regras
    rules_to_apply = [-1]
    
    while len(rules_to_apply) > 0:
        rules_to_apply = []
        for i, r in base_regras.iterrows():
            exp = parse_rule(r['ANTECEDENTE'])
            antecedent = evaluate_expressions(exp)
            consequent = r['CONSEQUENTE']
            if antecedent and consequent not in base_fatos.FATO.to_list():
                rules_to_apply.append(consequent)
        
        for rule in rules_to_apply:
            print(f'Foi descoberto que {rule} é verdade.')
            base_fatos.loc[len(base_fatos.index)] = [rule, 'True']

if __name__ == '__main__':
    print_yellow('                           Bem vindo ao Expert UFAL\n')
    print('Foi importada uma base de regras dos arquivos da pasta BaseDeConhecimento\n')
    print('Nesta base foram detectadas as seguintes proposições:', end=' ')
    fatos = scan()
    for fato in fatos:
        print(fato, end=', ')
    print()

    print()
    answer = input('Gostaria de ver as regras da base? (S/N)')
    if "S" in answer.upper():
        show_rules()

    q = read_question(fatos)
    global base_fatos, base_regras, explanation
    explanation = []
    base_fatos, base_regras = importKnowledgeBase()
    print('Gostaria de usar encadeamento para frente ou para trás?')
    choice = input('[1] Para Frente\n[2] Para trás\n[3] Misto')
    if choice == '1':
        infer_forwards()
    elif choice == '2':
        answer = infer_backwards(q)
        if answer:
            print_cyan(f"A seguinte sequência de regras confirmou que {q} é verdadeiro")
            
    else:
        infer_mixed()