import random
import numpy as np
import matplotlib.pyplot as plt

# Função para calcular a distância entre duas cidades
def calcular_distancia(cidade1, cidade2):
    return np.sqrt((cidade1[0] - cidade2[0])**2 + (cidade1[1] - cidade2[1])**2)

# Função para calcular o fitness de uma solução (distância total)
def calcular_fitness(rota, cidades):
    distancia_total = 0
    for i in range(len(rota) - 1):
        distancia_total += calcular_distancia(cidades[rota[i]], cidades[rota[i+1]])
    return distancia_total

# Função para inicializar uma população aleatória
def inicializar_populacao(num_individuos, num_cidades):
    populacao = []
    for _ in range(num_individuos):
        rota = list(range(num_cidades))
        random.shuffle(rota)
        populacao.append(rota)
    return populacao

# Função para realizar o cruzamento (recombinação) entre dois pais
def cruzamento(pai1, pai2):
    ponto_corte = random.randint(0, len(pai1) - 1)
    filho = pai1[:ponto_corte]
    for gene in pai2:
        if gene not in filho:
            filho.append(gene)
    return filho

# Função para realizar a mutação em um indivíduo
def mutacao(individuo, taxa_mutacao):
    if random.random() < taxa_mutacao:
        idx1, idx2 = random.sample(range(len(individuo)), 2)
        individuo[idx1], individuo[idx2] = individuo[idx2], individuo[idx1]

# Função para selecionar os melhores indivíduos para a próxima geração (elitismo)
def selecao_elitista(populacao, fitness_populacao, num_individuos):
    populacao_com_fitness = list(zip(populacao, fitness_populacao))
    populacao_com_fitness.sort(key=lambda x: x[1])
    melhores = [individuo for individuo, _ in populacao_com_fitness[:num_individuos]]
    return melhores

# Função principal para executar o algoritmo genético
def algoritmo_genetico(cidades, num_geracoes, tamanho_populacao, taxa_cruzamento, taxa_mutacao, taxa_elitismo):
    num_cidades = len(cidades)
    populacao = inicializar_populacao(tamanho_populacao, num_cidades)
    melhores_fitness = []
    fitness_medio_por_geracao = []
    piores_fitness = []
    
    for geracao in range(num_geracoes):
        fitness_populacao = [calcular_fitness(individuo, cidades) for individuo in populacao]
        melhores_fitness.append(min(fitness_populacao))
        piores_fitness.append(max(fitness_populacao))  # Calcule e armazene o pior fitness

        
        nova_populacao = selecao_elitista(populacao, fitness_populacao, int(tamanho_populacao * taxa_elitismo))
        
        while len(nova_populacao) < tamanho_populacao:
            pai1, pai2 = random.choices(populacao, k=2)
            filho = cruzamento(pai1, pai2)
            mutacao(filho, taxa_mutacao)
            nova_populacao.append(filho)
        
        populacao = nova_populacao

        # Calcula o fitness médio da população atual e o armazena em fitness_medio_por_geracao
        fitness_medio_por_geracao_execucao = np.mean(fitness_populacao)
        fitness_medio_por_geracao.append(fitness_medio_por_geracao_execucao)
    
    melhor_rota = populacao[fitness_populacao.index(min(fitness_populacao))]
    melhor_distancia = min(fitness_populacao)
    
    return melhor_rota, melhor_distancia, melhores_fitness, fitness_medio_por_geracao, piores_fitness

# Leitura das coordenadas das cidades a partir do arquivo cidades.txt
def ler_cidades(filename):
    cidades = []
    with open(filename, 'r') as file:
        for line in file:
            x, y = map(float, line.strip().split())
            cidades.append((x, y))
    return cidades

if __name__ == "__main__":
    # Parâmetros do AG
    num_geracoes = 100
    num_execucoes = 10  # Número de execuções do algoritmo
    tamanho_populacao = 100
    taxa_cruzamento = 0.7
    taxa_mutacao = 0.01
    taxa_elitismo = 0.05

    # Leitura das coordenadas das cidades a partir do arquivo cidades.txt
    cidades = ler_cidades('cidades.txt')

    melhores_solucoes = []  # Para armazenar as melhores soluções de cada execução
    fitness_medio_por_execucao = []
    fitness_melhor_por_execucao = []
    fitness_pior_por_execucao = []

    # Define uma lista de símbolos diferentes para cada série de dados
    simbolos = ['o', 's', '^', 'D', 'v', 'p', '*', '+', 'x', 'H']
    geracoes = range(num_geracoes)

    for execucao in range(num_execucoes):
       # Execução do Algoritmo Genético
        melhor_rota, melhor_distancia, melhores_fitness, fitness_medio, fitness_pior = algoritmo_genetico(
            cidades, num_geracoes, tamanho_populacao, taxa_cruzamento, taxa_mutacao, taxa_elitismo
        )
        melhores_solucoes.append((melhor_rota, melhor_distancia))
        
        # Registra o fitness médio, melhor e pior por geração para esta execução
        fitness_medio_por_execucao.append(fitness_medio)
        fitness_melhor_por_execucao.append([min(melhores_fitness[:i+1]) for i in range(num_geracoes)])
        fitness_pior_por_execucao.append(fitness_pior)

        # Plota um gráfico separado para esta execução
        plt.figure(figsize=(12, 6))
        
        plt.plot(geracoes, fitness_melhor_por_execucao[execucao], label=f'Melhor Fitness', marker=simbolos[1])
        plt.plot(geracoes, fitness_pior_por_execucao[execucao], label=f'Pior Fitness', marker=simbolos[2])
        plt.plot(geracoes, fitness_medio, label=f'Fitness Médio', marker=simbolos[0])
        plt.xlabel('Gerações')
        plt.ylabel('Fitness (Distância Total)')
        plt.title(f'Curvas de Fitness Execução {execucao+1}')
        plt.legend()

        # Salva o gráfico em um arquivo PNG com o número da execução
        nome_arquivo_png = f'execucao_{execucao+1}.png'
        plt.savefig(nome_arquivo_png)

        # Fecha a figura para liberar memória
        plt.close()

    # Cálculo do valor médio e desvio padrão das distâncias totais das melhores soluções
    distancias_melhores_solucoes = [solucao[1] for solucao in melhores_solucoes]
    media_distancias = np.mean(distancias_melhores_solucoes)
    desvio_padrao_distancias = np.std(distancias_melhores_solucoes)

    # Calcula o valor médio e desvio padrão dos fitness das soluções finais
    media_fitness = np.mean(distancias_melhores_solucoes)
    desvio_padrao_fitness = np.std(distancias_melhores_solucoes)
    # Grava os resultados das melhores soluções e os valores médio e desvio padrão dos fitness em um arquivo CSV
    with open('melhores_solucoes.csv', 'w') as arquivo_csv:
        arquivo_csv.write('Execucao,MelhorDistancia,Media das Melhores Distancias,Desvio Padrao das Melhores Distancias,Media dos Fitness das Soluçoes Finais,Desvio Padrao dos Fitness das Soluçoes Finais\n')
        for execucao, distancia in enumerate(distancias_melhores_solucoes, 1):
            arquivo_csv.write(f'{execucao},{distancia},{media_distancias},{desvio_padrao_distancias},{media_fitness},{desvio_padrao_fitness}\n')

    # Imprime os resultados
    print(f'Média das Melhores Distâncias: {media_distancias}')
    print(f'Desvio Padrão das Melhores Distâncias: {desvio_padrao_distancias}')
    print(f'Média dos Fitness das Soluções Finais: {media_fitness}')
    print(f'Desvio Padrão dos Fitness das Soluções Finais: {desvio_padrao_fitness}')


    # Plotagem das curvas de fitness médio, melhor e pior por geração para cada execução
    geracoes = range(num_geracoes)
   
    plt.figure(figsize=(12, 6))
    for execucao in range(num_execucoes):
        plt.plot(geracoes, fitness_medio_por_execucao[execucao], label=f'Fitness Médio - Execução {execucao+1}')
        plt.plot(geracoes, fitness_melhor_por_execucao[execucao], label=f'Melhor Fitness - Execução {execucao+1}')
        plt.plot(geracoes, fitness_pior_por_execucao[execucao], label=f'Pior Fitness - Execução {execucao+1}')
    plt.xlabel('Gerações')
    plt.ylabel('Fitness (Distância Total)')
    plt.title('Curvas de Fitness Médio, Melhor e Pior por Geração')
    plt.legend()
    plt.show()
