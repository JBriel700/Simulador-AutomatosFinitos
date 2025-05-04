# Simulador de Autômatos Finitos

## Sobre

Simulador de automatos finitos. Recebe um arquivo no formato JSON contendo as transições de estados e outro no formato CSV 
contendo as palavras de entrada e o resultado esperado (1 - Aceita/0 - Rejeita). Em seguida, gera um arquivo de saída contendo
as palavra de entrada, os resultados esperados, os resultados obtidos e o tempo de execução.

# Funcionamento!

### 1. O programa verifica os argumentos e carrega o autômato. 
```python
if len(sys.argv) != 4:
    sys.exit()

try:
    with open(sys.argv[1], 'r') as arquivo:
        automato = json.load(arquivo)
except:
    sys.exit()
````

### 2. Abre o arquivo de teste para leitura e o arquivo de saída para escrita. Remove espaços em branco e Ignora linhas vazias ou linhas sem o separador ; para cada linha do arquivo de testes.
```python
try:
    with open(sys.argv[2], 'r') as testes, open(sys.argv[3], 'w') as saida:
        for linha in testes:
            linha = linha.strip()
            if not linha or ';' not in linha:
                continue
````

### 3. Separa a palavra de teste e o valor esperado, inicializa o conjunto de estados, marca o início do tempo de processamento e aplica as transições que não consomem símbolo.
```python
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
````

### 4. Busca possíveis transições a partir dos estados atuais. Se não encontrar, marca a palavra como inválida. Atualiza o conjunto de estados alcançados e aplica novamente as transições vazias após cada símbolo.
```python
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

````

### 5. Verifica se um dos estados atuais é final e salva as palavras de entrada, resultados esperados, resultados obtidos e tempo de execução.
```python
ceito = any(estado in automato["final"] for estado in estados) if valido else False
            
saida.write(f"{palavra};{esperado};{1 if aceito else 0};{time.time() - inicio:.6f}\n")

````

### 6 - Se houver alguma erro durante a execução do processamento, exibe a mensagem "Erro." no terminal e finaliza o programa. Caso contrátio, exibe "sucesso!".
```python
except:
    print("Erro.")
    sys.exit()

print("sucesso!")
````


## Como usar

O programa é executado pelo comando: 

```bash
python main.py estados.aut teste.in resultado.out
