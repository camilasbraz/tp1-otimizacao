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
    num_execucoes = 1  # Número de execuções do algoritmo
    tamanho_populacao = 100
    taxa_cruzamento = 0.7
    taxa_mutacao = 0.01
    taxa_elitismo = 0.05

    # Leitura das coordenadas das cidades a partir do arquivo cidades.txt
    cidades = ler_cidades('cidades.txt')

    # Define as faixas de valores para os parâmetros
    faixa_tamanho_populacao = range(10, 101, 10)
    faixa_num_geracoes = range(10, 51, 10)
    faixa_taxa_cruzamento = [0.6, 0.65, 0.7, 0.75, 0.8]
    faixa_taxa_mutacao = [0.01, 0.02, 0.03, 0.04, 0.05]
    faixa_taxa_elitismo = [0.55, 0.6, 0.65, 0.7, 0.75]

    # Leitura das coordenadas das cidades a partir do arquivo cidades.txt
    cidades = ler_cidades('cidades.txt')

    # Dicionário de parâmetros com as faixas de valores
    parametros = {
        'Tamanho da População': faixa_tamanho_populacao,
        'Número Máximo de Gerações': faixa_num_geracoes,
        'Taxa de Cruzamento': faixa_taxa_cruzamento,
        'Taxa de Mutação': faixa_taxa_mutacao,
        'Taxa de Elitismo': faixa_taxa_elitismo,
    }
    
    # Loop através dos parâmetros
    for nome_parametro in parametros:
        if nome_parametro == 'Tamanho da População':
            faixa_valores = faixa_tamanho_populacao
            fitness_data = {}
            for valor_parametro in faixa_valores:
                # Defina o valor do parâmetro
                tamanho_populacao = valor_parametro
                num_geracoes = 100
                taxa_cruzamento = 0.7
                taxa_mutacao = 0.01
                taxa_elitismo = 0.05
                # Execução do Algoritmo Genético
                _, _, _, fitness_medio, _ = algoritmo_genetico(
                    cidades, num_geracoes, tamanho_populacao, taxa_cruzamento, taxa_mutacao, taxa_elitismo
                )

                fitness_data[tamanho_populacao] = fitness_medio
                # Plota um gráfico para esta combinação de parâmetros
            geracoes = range(num_geracoes)

            plt.figure(figsize=(12, 6))
            for tamanho_populacao, fitness_medio in fitness_data.items():
                plt.plot(geracoes, fitness_medio, label=f'Tamanho da População {tamanho_populacao}')

            plt.xlabel('Gerações')
            plt.ylabel('Média de Fitness (Distância Total)')
            plt.title('Evolução da Média de Fitness para Diferentes Tamanhos de População')
            plt.legend()
            

            # Salva o gráfico em um arquivo PNG com o valor do parâmetro
            nome_arquivo_png = f'tamanho_populacao_caixeiro.png'
            plt.savefig(nome_arquivo_png)

            # Fecha a figura para liberar memória
            plt.close()
        # elif nome_parametro == 'Número Máximo de Gerações':
        #     for valor_parametro in faixa_valores:
        #         faixa_valores = faixa_num_geracoes
        #         fitness_data = {}
        #         for valor_parametro in faixa_valores:
        #             # Defina o valor do parâmetro
        #             num_geracoes = valor_parametro
        #             tamanho_populacao = 100
        #             taxa_cruzamento = 0.7
        #             taxa_mutacao = 0.01
        #             taxa_elitismo = 0.05
        #             # Execução do Algoritmo Genético
        #             _, _, _, fitness_medio, _ = algoritmo_genetico(
        #                 cidades, num_geracoes, tamanho_populacao, taxa_cruzamento, taxa_mutacao, taxa_elitismo
        #             )

        #             fitness_data[num_geracoes] = fitness_medio
        #             # Plota um gráfico para esta combinação de parâmetros
        #         geracoes = range(num_geracoes)

        #         plt.figure(figsize=(12, 6))
        #         for num_geracoes, fitness_medio in fitness_data.items():
        #             plt.plot(geracoes, fitness_medio, label=f'Número Máximo de Gerações: {num_geracoes}')

        #         plt.xlabel('Gerações')
        #         plt.ylabel('Média de Fitness (Distância Total)')
        #         plt.title('Evolução da Média de Fitness para Diferentes Números Máximos de Gerações')
        #         plt.legend()
                

        #         # Salva o gráfico em um arquivo PNG com o valor do parâmetro
        #         nome_arquivo_png = f'num_geracoes_caixeiro.png'
        #         plt.savefig(nome_arquivo_png)

        #         # Fecha a figura para liberar memória
        #         plt.close()
        elif nome_parametro == 'Taxa de Cruzamento':
            faixa_valores = faixa_taxa_cruzamento
            fitness_data = {}
            for valor_parametro in faixa_valores:
                # Defina o valor do parâmetro
                fitness_medio_parametro = []  # Lista para armazenar os resultados do fitness médio
                taxa_cruzamento = valor_parametro
                num_geracoes = 100
                tamanho_populacao = 100
                taxa_mutacao = 0.01
                taxa_elitismo = 0.05
                # Execução do Algoritmo Genético
                _, _, _, fitness_medio, _ = algoritmo_genetico(
                    cidades, num_geracoes, tamanho_populacao, taxa_cruzamento, taxa_mutacao, taxa_elitismo
                )

                fitness_data[taxa_cruzamento] = fitness_medio
                # Plota um gráfico para esta combinação de parâmetros
            geracoes = range(num_geracoes)

            plt.figure(figsize=(12, 6))
            for taxa_cruzamento, fitness_medio in fitness_data.items():
                plt.plot(geracoes, fitness_medio, label=f'Taxa de Cruzamento: {taxa_cruzamento}')

            plt.xlabel('Gerações')
            plt.ylabel('Média de Fitness (Distância Total)')
            plt.title('Evolução da Média de Fitness para Diferentes Taxas de Cruzamento')
            plt.legend()
           

            # Salva o gráfico em um arquivo PNG com o valor do parâmetro
            nome_arquivo_png = f'taxa_cruzamento_caixeiro.png'
            plt.savefig(nome_arquivo_png)

            # Fecha a figura para liberar memória
            plt.close()
        elif nome_parametro == 'Taxa de Mutação':
            faixa_valores = faixa_taxa_mutacao
            fitness_data = {}
            for valor_parametro in faixa_valores:
                # Defina o valor do parâmetro
                fitness_medio_parametro = []  # Lista para armazenar os resultados do fitness médio
                taxa_mutacao = valor_parametro
                num_geracoes = 100
                tamanho_populacao = 100
                taxa_cruzamento = 0.7
                taxa_elitismo = 0.05
                # Execução do Algoritmo Genético
                _, _, _, fitness_medio, _ = algoritmo_genetico(
                    cidades, num_geracoes, tamanho_populacao, taxa_cruzamento, taxa_mutacao, taxa_elitismo
                )
                fitness_data[taxa_mutacao] = fitness_medio

            geracoes = range(num_geracoes)

            plt.figure(figsize=(12, 6))
            for taxa_mutacao, fitness_medio in fitness_data.items():
                plt.plot(geracoes, fitness_medio, label=f'Taxa de Mutação {taxa_mutacao}')

            plt.xlabel('Gerações')
            plt.ylabel('Média de Fitness (Distância Total)')
            plt.title('Evolução da Média de Fitness para Diferentes Taxas de Mutação')
            plt.legend()
            

            # Salva o gráfico em um arquivo PNG com o valor do parâmetro
            nome_arquivo_png = f'taxa_mutacao_caixeiro.png'
            plt.savefig(nome_arquivo_png)

            # Fecha a figura para liberar memória
            plt.close()
        elif nome_parametro == 'Taxa de Elitismo':
            faixa_valores = faixa_taxa_elitismo
            fitness_data = {}
            for valor_parametro in faixa_valores:
                # Defina o valor do parâmetro
                fitness_medio_parametro = []  # Lista para armazenar os resultados do fitness médio
                taxa_elitismo = valor_parametro
                num_geracoes = 100
                tamanho_populacao = 100
                taxa_cruzamento = 0.7
                taxa_mutacao = 0.01
                # Execução do Algoritmo Genético
                _, _, _, fitness_medio, _ = algoritmo_genetico(
                    cidades, num_geracoes, tamanho_populacao, taxa_cruzamento, taxa_mutacao, taxa_elitismo
                )
                fitness_data[taxa_elitismo] = fitness_medio
            
            geracoes = range(num_geracoes)

            plt.figure(figsize=(12, 6))
            for taxa_elitismo, fitness_medio in fitness_data.items():
                plt.plot(geracoes, fitness_medio, label=f'Taxa de Elitismo: {taxa_elitismo}')

            plt.xlabel('Gerações')
            plt.ylabel('Média de Fitness (Distância Total)')
            plt.title('Evolução da Média de Fitness para Diferentes Taxas de Elitismo')
            plt.legend()
           

            # Salva o gráfico em um arquivo PNG com o valor do parâmetro
            nome_arquivo_png = f'taxa_elitismo_caixeiro.png'
            plt.savefig(nome_arquivo_png)

            # Fecha a figura para liberar memória
            plt.close()


    # # Define as faixas de valores para os parâmetros
    # faixa_tamanho_populacao = range(10, 101, 10)
    # faixa_tamanho_cromossomo = range(10, 36, 5)
    # faixa_num_geracoes = range(10, 51, 10)
    # faixa_taxa_cruzamento = [0.6, 0.65, 0.7, 0.75, 0.8]
    # faixa_taxa_mutacao = [0.01, 0.02, 0.03, 0.04, 0.05]
    # faixa_taxa_elitismo = [0.55, 0.6, 0.65, 0.7, 0.75]

    

    # melhores_solucoes = []  # Para armazenar as melhores soluções de cada execução
    # fitness_medio_por_execucao = []
    # fitness_melhor_por_execucao = []
    # fitness_pior_por_execucao = []

    # # Define uma lista de símbolos diferentes para cada série de dados
    # simbolos = ['o', 's', '^', 'D', 'v', 'p', '*', '+', 'x', 'H']
    # geracoes = range(num_geracoes)

    # for execucao in range(num_execucoes):
    #    # Execução do Algoritmo Genético
    #     melhor_rota, melhor_distancia, melhores_fitness, fitness_medio, fitness_pior = algoritmo_genetico(
    #         cidades, num_geracoes, tamanho_populacao, taxa_cruzamento, taxa_mutacao, taxa_elitismo
    #     )
    #     melhores_solucoes.append((melhor_rota, melhor_distancia))
        
    #     # Registra o fitness médio, melhor e pior por geração para esta execução
    #     fitness_medio_por_execucao.append(fitness_medio)
    #     fitness_melhor_por_execucao.append([min(melhores_fitness[:i+1]) for i in range(num_geracoes)])
    #     fitness_pior_por_execucao.append(fitness_pior)

    #     # Plota um gráfico separado para esta execução
    #     plt.figure(figsize=(12, 6))
        
    #     plt.plot(geracoes, fitness_melhor_por_execucao[execucao], label=f'Melhor Fitness', marker=simbolos[1])
    #     plt.plot(geracoes, fitness_pior_por_execucao[execucao], label=f'Pior Fitness', marker=simbolos[2])
    #     plt.plot(geracoes, fitness_medio, label=f'Fitness Médio', marker=simbolos[0])
    #     plt.xlabel('Gerações')
    #     plt.ylabel('Fitness (Distância Total)')
    #     plt.title(f'Curvas de Fitness Execução {execucao+1}')
    #     plt.legend()

    #     # Salva o gráfico em um arquivo PNG com o número da execução
    #     nome_arquivo_png = f'execucao_{execucao+1}.png'
    #     plt.savefig(nome_arquivo_png)

    #     # Fecha a figura para liberar memória
    #     plt.close()

    # # Cálculo do valor médio e desvio padrão das distâncias totais das melhores soluções
    # distancias_melhores_solucoes = [solucao[1] for solucao in melhores_solucoes]
    # media_distancias = np.mean(distancias_melhores_solucoes)
    # desvio_padrao_distancias = np.std(distancias_melhores_solucoes)

    # # Calcula o valor médio e desvio padrão dos fitness das soluções finais
    # media_fitness = np.mean(distancias_melhores_solucoes)
    # desvio_padrao_fitness = np.std(distancias_melhores_solucoes)
    # # Grava os resultados das melhores soluções e os valores médio e desvio padrão dos fitness em um arquivo CSV
    # with open('melhores_solucoes.csv', 'w') as arquivo_csv:
    #     arquivo_csv.write('Execucao,MelhorDistancia,Media das Melhores Distancias,Desvio Padrao das Melhores Distancias,Media dos Fitness das Soluçoes Finais,Desvio Padrao dos Fitness das Soluçoes Finais\n')
    #     for execucao, distancia in enumerate(distancias_melhores_solucoes, 1):
    #         arquivo_csv.write(f'{execucao},{distancia},{media_distancias},{desvio_padrao_distancias},{media_fitness},{desvio_padrao_fitness}\n')

    # # Imprime os resultados
    # print(f'Média das Melhores Distâncias: {media_distancias}')
    # print(f'Desvio Padrão das Melhores Distâncias: {desvio_padrao_distancias}')
    # print(f'Média dos Fitness das Soluções Finais: {media_fitness}')
    # print(f'Desvio Padrão dos Fitness das Soluções Finais: {desvio_padrao_fitness}')


    # # Plotagem das curvas de fitness médio, melhor e pior por geração para cada execução
    # geracoes = range(num_geracoes)
   
    # plt.figure(figsize=(12, 6))
    # for execucao in range(num_execucoes):
    #     plt.plot(geracoes, fitness_medio_por_execucao[execucao], label=f'Fitness Médio - Execução {execucao+1}')
    #     plt.plot(geracoes, fitness_melhor_por_execucao[execucao], label=f'Melhor Fitness - Execução {execucao+1}')
    #     plt.plot(geracoes, fitness_pior_por_execucao[execucao], label=f'Pior Fitness - Execução {execucao+1}')
    # plt.xlabel('Gerações')
    # plt.ylabel('Fitness (Distância Total)')
    # plt.title('Curvas de Fitness Médio, Melhor e Pior por Geração')
    # plt.legend()
    # plt.show()
