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
    
    for geracao in range(num_geracoes):
        fitness_populacao = [calcular_fitness(individuo, cidades) for individuo in populacao]
        melhores_fitness.append(min(fitness_populacao))
        
        nova_populacao = selecao_elitista(populacao, fitness_populacao, int(tamanho_populacao * taxa_elitismo))
        
        while len(nova_populacao) < tamanho_populacao:
            pai1, pai2 = random.choices(populacao, k=2)
            filho = cruzamento(pai1, pai2)
            mutacao(filho, taxa_mutacao)
            nova_populacao.append(filho)
        
        populacao = nova_populacao
    
    melhor_rota = populacao[fitness_populacao.index(min(fitness_populacao))]
    melhor_distancia = min(fitness_populacao)
    
    return melhor_rota, melhor_distancia, melhores_fitness

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
    tamanho_populacao = 100
    taxa_cruzamento = 0.7
    taxa_mutacao = 0.01
    taxa_elitismo = 0.05

    # Leitura das coordenadas das cidades a partir do arquivo cidades.txt
    cidades = ler_cidades('cidades.txt')

    # Execução do Algoritmo Genético
    melhor_rota, melhor_distancia, melhores_fitness = algoritmo_genetico(
        cidades, num_geracoes, tamanho_populacao, taxa_cruzamento, taxa_mutacao, taxa_elitismo
    )

    print(f'Melhor Rota Encontrada: {melhor_rota}')
    print(f'Distância Total: {melhor_distancia}')

    # Plotagem da evolução do fitness
    plt.plot(melhores_fitness)
    plt.xlabel('Gerações')
    plt.ylabel('Fitness (Distância Total)')
    plt.title('Evolução do Fitness no Algoritmo Genético')
    plt.show()
