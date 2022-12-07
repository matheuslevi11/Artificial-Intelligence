from style import *
from utils import *

def ask(fact, i):
    if fact == "CANSACO":
        fact = "Cansaço"
    elif "_" in fact:
        fact = fact.replace('_', ' ').capitalize()
    else:
        fact = fact.capitalize()
    print_yellow(f'Você possui o seguinte sintoma? {fact}')
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
                value = ask(e, i).upper()
                str_value = 'True' if value == 'V' else 'False'
                value = True if str_value == 'True' else False
                base_fatos.loc[len(base_fatos.index)] = [e, str_value]
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

def infer_forwards():
    global base_fatos, base_regras, classes, readable_classes, explanation

    for i, r in base_regras.iterrows():
        consequent = r['CONSEQUENTE']
        exp = parse_rule(r['ANTECEDENTE'])
        antecedent = evaluate_expressions(exp)
        if antecedent:
            if consequent not in base_fatos.FATO.to_list():
                base_fatos.loc[len(base_fatos.index)] = [consequent, 'True']
                explanation.append((r['ANTECEDENTE'], r['CONSEQUENTE']))
            if consequent in classes:
                print_green(f'A seu diagnóstico é: {readable_classes[classes.index(consequent)].capitalize()} com {r["FC"]}% de confiança.')
                return True
    return False

def guess():
    global base_regras, base_fatos, readable_classes, explanation
    explanation = []
    base_fatos, base_regras = importKnowledgeBase(facts="work_memory", rules="regras")
    if not infer_forwards():
        print_red("Não consegui te diagnosticar :(")
    else:
        print_yellow('--------------------------------------------------------------------------')
        print_cyan('Cheguei a esta conclusão pelos seguintes motivos:')
        for rule, conclusion in explanation:
            rule = rule.replace(' ', '').split('and')
            print("Por essas características:", end=' ')
            for r in rule:
                print(f'{r.replace("_", " ").capitalize()}, ', end='')
            print(f'conclui-se que é {readable_classes[classes.index(conclusion)].capitalize()}')

if __name__ == '__main__':
    global classes, readable_classes
    classes = ['GRIPE', 'MONONUCLEOSE_INFECCIOSA', 'AMIGDALITE', 'ESTRESSE', 'RINITE_ALERGICA', 'COVID19']
    readable_classes = ['Gripe', 'Mononucleose Infecciosa', 'Amigdalite', 'Estresse', 'Rinite Alérgica', 'COVID-19']
    
    print_yellow('--------------------------------------------------------------------------')
    print_yellow('Bem vindo ao Diagnóstico Médico')
    print_yellow('--------------------------------------------------------------------------')
    ok = ''
    while ok.lower() != 'ok':
        ok = input('Digite ok para iniciar:')
    
    guess()