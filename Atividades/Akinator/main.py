from style import *
from utils import *

def ask(fact):
    if fact == "!VOA":
        fact = "não voa"
    elif "_" in fact:
        fact = fact.replace('_', ' ').capitalize()
    else:
        fact = fact.capitalize()
    print_yellow(f'O animal que você pensou tem a seguinte característica? {fact}')
    answer = ''
    while answer.upper() != 'V' and answer.upper() != 'F':
        answer = input('(V/F)')
    return answer

def parse_rule(rule):
    global base_fatos, base_regras
    rule = rule.split(' ')

    for i in range(len(rule)):
        e = rule[i]
        if e != 'and' and e != 'or':
            if e in base_fatos.FATO.to_list():
                value = base_fatos[base_fatos.FATO == e].values[0][1] 
                value = True if value == 'True' else False
            else:
                value = ask(e).upper()
                str_value = 'True' if value == 'V' else 'False'
                value = True if str_value == 'True' else False
                base_fatos.loc[len(base_fatos.index)] = [e, str_value]
                if value:
                    grow_knowledge(e)
            rule[i] = value
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

def grow_knowledge(fact):
    global base_fatos, base_regras, fact_list, explanation
    for i, r in base_regras.iterrows():
        antecedent = r['ANTECEDENTE']
        consequent = r['CONSEQUENTE']
        if consequent not in base_fatos.FATO.to_list():
            if fact in antecedent:
                rule = antecedent.split(' ')
                for i in range(len(rule)):
                    e = rule[i]
                    if e != 'and' and e != 'or':
                        if e in base_fatos.FATO.to_list():
                            value = base_fatos[base_fatos.FATO == e].values[0][1]
                            value = True if value == 'True' else False
                        else:
                            return False
                        
                        rule[i] = value
                if evaluate_expressions(rule):
                    base_fatos.loc[len(base_fatos.index)] = [consequent, 'True']
                    explanation.append((antecedent, consequent))
                    if consequent in fact_list:
                        print_green(f'O animal que você imaginou é: {consequent.capitalize()}')
                        print_yellow('--------------------------------------------------------------------------')
                        print_cyan('Cheguei a esta conclusão pelos seguintes motivos:')
                        for rule, conclusion in explanation:
                            rule = rule.replace(' ', '').split('and')
                            print("Por essas características:", end=' ')
                            for r in rule:
                                print(f'{r.capitalize()}, ', end='')
                            print(f'conclui-se que é {conclusion.capitalize()}')
                        exit()

    return False

def infer_forwards():
    global base_fatos, base_regras, fact_list, explanation
    discovered = [-1]

    while len(discovered) > 0:
        discovered = []
        for i, r in base_regras.iterrows():
            consequent = r['CONSEQUENTE']
            if consequent not in base_fatos.FATO.to_list():
                exp = parse_rule(r['ANTECEDENTE'])
                antecedent = evaluate_expressions(exp)
                if antecedent:
                    if consequent not in base_fatos.FATO.to_list():
                        base_fatos.loc[len(base_fatos.index)] = [consequent, 'True']
                        explanation.append((r['ANTECEDENTE'], r['CONSEQUENTE']))
                    grow_knowledge(consequent)
                    discovered.append(consequent)
                    if consequent in fact_list:
                        print_green(f'O animal que você imaginou é: {consequent.capitalize()}')
                        return True
    return False

def guess():
    global base_regras, base_fatos, explanation
    explanation = []
    base_fatos, base_regras = importKnowledgeBase(facts="work_memory", rules="animais")
    if not infer_forwards():
        print_red("Não consegui adivinhar qual animal você pensou :(")
    else:
        print_yellow('--------------------------------------------------------------------------')
        print_cyan('Cheguei a esta conclusão pelos seguintes motivos:')
        for rule, conclusion in explanation:
            rule = rule.replace(' ', '').split('and')
            print("Por essas características:", end=' ')
            for r in rule:
                print(f'{r.capitalize()}, ', end='')
            print(f',conclui-se que é {conclusion.capitalize()}')
            
if __name__ == '__main__':
    global fact_list
    animals = ["Leopardo", "Tigre", "Girafa", "Zebra", "Avestruz", "Pinguim", "Albatroz", "Galinha", "Flamingo", "Urso"]
    fact_list = [a.upper() for a in animals]
    
    print_yellow('--------------------------------------------------------------------------')
    print_yellow('Bem vindo ao Animal Akinator')
    print_yellow('--------------------------------------------------------------------------')
    print('Escolha um dos seguintes animais e pense nele:\n')
    
    for i, animal in enumerate(animals):
        print_purple(f"[{i+1}] {animal}")
    print("\n")

    print_cyan("Pensou?")
    ok = ''
    while ok.lower() != 'ok':
        ok = input('Digite ok para iniciar:')
    
    guess()