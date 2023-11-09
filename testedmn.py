import pyDMNrules

# Criar uma instância da classe DMN
dmn = pyDMNrules.DMN()

# Carregar a tabela de decisão do arquivo CSV
dmn.load("desconto.csv")

# Definir os dados de entrada
entrada = {"preco": 150, "categoria": "eletronico"}

# Executar a tabela de decisão e obter o resultado
resultado = dmn.decide(entrada)

# Imprimir o resultado
print(resultado)