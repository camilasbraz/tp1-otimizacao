import random

class Item:
    def __init__(self, peso, valor):
        self.peso = peso
        self.valor = valor

class MochilaGenetica:
    def __init__(self, tamanho_mochila, itens):
        self.tamanho_mochila = tamanho_mochila
        self.itens = itens
        self.tamanho_populacao = 100
        self.taxa_cruzamento = 0.8
        self.taxa_mutacao = 0.1
        self.taxa_elitismo = 0.1
        self.num_geracoes = 100

    def criar_cromossomo(self):
        return [random.randint(0, 1) for _ in range(len(self.itens))]

    def calcular_fitness(self, cromossomo):
        peso_total = sum(cromossomo[i] * self.itens[i].peso for i in range(len(cromossomo)))
        valor_total = sum(cromossomo[i] * self.itens[i].valor for i in range(len(cromossomo)))
        if peso_total > self.tamanho_mochila:
            return 0
        else:
            return valor_total

    def selecao(self, populacao):
        pesos_fitness = [self.calcular_fitness(cromossomo) for cromossomo in populacao]

        # Verificando se todos os pesos são zero
        if sum(pesos_fitness) == 0:
            return random.choices(populacao, k=self.tamanho_populacao)
        else:
            return random.choices(populacao, weights=pesos_fitness, k=self.tamanho_populacao)

    def cruzamento(self, pai1, pai2):
        ponto_corte = random.randint(1, len(pai1) - 1)
        filho1 = pai1[:ponto_corte] + pai2[ponto_corte:]
        filho2 = pai2[:ponto_corte] + pai1[ponto_corte:]
        return filho1, filho2

    def mutacao(self, cromossomo):
        indice = random.randint(0, len(cromossomo) - 1)
        cromossomo[indice] = 1 - cromossomo[indice]
        return cromossomo

    def algoritmo_genetico(self):
        populacao = [self.criar_cromossomo() for _ in range(self.tamanho_populacao)]

        for _ in range(self.num_geracoes):
            populacao = self.selecao(populacao)

            for i in range(0, self.tamanho_populacao, 2):
                pai1, pai2 = random.choices(populacao, k=2)
                if random.random() < self.taxa_cruzamento:
                    filho1, filho2 = self.cruzamento(pai1, pai2)
                    populacao += [filho1, filho2]

            for i in range(len(populacao)):
                if random.random() < self.taxa_mutacao:
                    populacao[i] = self.mutacao(populacao[i])

            num_elites = int(self.taxa_elitismo * self.tamanho_populacao)
            melhores_indices = sorted(range(self.tamanho_populacao), key=lambda i: self.calcular_fitness(populacao[i]), reverse=True)[:num_elites]
            elite = [populacao[i] for i in melhores_indices]
            populacao = elite + random.choices(populacao, k=self.tamanho_populacao - num_elites)

        melhor_cromossomo = max(populacao, key=self.calcular_fitness)
        melhor_valor = self.calcular_fitness(melhor_cromossomo)
        return melhor_cromossomo, melhor_valor

