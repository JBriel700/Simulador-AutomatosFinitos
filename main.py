import json
import sys
import time

if len(sys.argv) != 4:
    sys.exit()

try:
    with open(sys.argv[1], 'r') as arquivo:
        automato = json.load(arquivo)
except:
    sys.exit()

try:
    with open(sys.argv[2], 'r') as testes, open(sys.argv[3], 'w') as saida:
        for linha in testes:
            linha = linha.strip()
            if not linha or ';' not in linha:
                continue

            palavra, esperado = linha.split(';')
            estados = {automato["initial"]}
            valido = True
            inicio = time.time()

            novos_estados = set()
            for estado in estados:
                for trans in automato["transitions"]:
                    if trans["from"] == estado and trans["read"] is None:
                        novos_estados.add(trans["to"])
            estados.update(novos_estados)


            for simbolo in palavra:
                novos_estados = set()
                for estado in estados:
                    for trans in automato["transitions"]:
                        if trans["from"] == estado and trans["read"] == simbolo:
                            novos_estados.add(trans["to"])
                
                if not novos_estados:
                    valido = False
                    break
                
                estados = novos_estados
                
                novos_estados = set()
                for estado in estados:
                    for trans in automato["transitions"]:
                        if trans["from"] == estado and trans["read"] is None:
                            novos_estados.add(trans["to"])
                estados.update(novos_estados)

            aceito = any(estado in automato["final"] for estado in estados) if valido else False
            
            saida.write(f"{palavra};{esperado};{1 if aceito else 0};{time.time() - inicio:.6f}\n")

except:
    print("Erro.")
    sys.exit()

print("sucesso!")
