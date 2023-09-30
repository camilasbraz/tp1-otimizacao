from mochila import MochilaGenetica, Item
import random
from utils import loading_bar
from tqdm import tqdm
import pandas as pd
import os

class Experimento:
    def __init__(self, num_experimentos=10, save_results_path='./resultados'):
        self.num_experimentos = num_experimentos
        self.save_results_path = save_results_path
        self.resultados = []

    def criar_itens(self):
        loading_bar('Criando itens', 'red', '- criando itens da mochila -')
        return [Item(peso=random.randint(1, 10),
                     valor=random.randint(1, 100))
                for _ in range(20)]

    def criar_mochila(self, itens):
        loading_bar('Criando mochila', 'red', '- criando mochila -')
        return MochilaGenetica(10, itens)

    def salvar_resultados(self):
        # Cria um DataFrame do Pandas com os resultados
        df = pd.DataFrame(self.resultados, columns=['Melhor Cromossomo', 'Melhor Valor', 'Tamanho da População', 'Taxa de Cruzamento', 'Taxa de Mutação', 'Taxa de Elitismo'])

        # Salva o DataFrame em um arquivo CSV
        save_path = os.path.join(self.save_results_path, 'resultados_problema_mochila.csv')
        df.to_csv(save_path, index=False)
        print(df)
        print(f"Resultados salvos em {self.save_results_path}.")

    def executar_experimentos(self):
        print('\n----------------------------------------------')
        print(' PROBLEMA DA MOCHILA COM ALGORITMOS GENÉTICOS ')
        print('----------------------------------------------\n\n')
        melhor_resultado = None

        for i in range(self.num_experimentos):
            print(f' ---- EXPERIMENTO NUMERO {i} ----')
            itens = self.criar_itens()
            mochila = self.criar_mochila(itens)
            print('\n')

            # Inicialize a barra de progresso com 0%
            print('- executando experimento - ')
            barra_progresso = tqdm(total=4, desc='Executando experimento', bar_format="{desc}: {percentage:3.0f}% {bar}", colour='red')

            # Executando o algoritmo genético com diferentes combinações de parâmetros
            for tamanho_populacao in [50, 100, 200]:
                for taxa_cruzamento in [0.6, 0.8, 1.0]:
                    for taxa_mutacao in [0.05, 0.1, 0.2]:
                        for taxa_elitismo in [0.1, 0.2, 0.3]:

                            mochila.tamanho_populacao = tamanho_populacao
                            mochila.taxa_cruzamento = taxa_cruzamento
                            mochila.taxa_mutacao = taxa_mutacao
                            mochila.taxa_elitismo = taxa_elitismo

                            mochila.num_geracoes = 100  # Número fixo de gerações para simplificar o exemplo

                            # Executando o algoritmo genético
                            melhor_cromossomo, melhor_valor = mochila.algoritmo_genetico()

                            # Armazenando o melhor resultado
                            if melhor_resultado is None or melhor_valor > melhor_resultado[1]:
                                melhor_resultado = (melhor_cromossomo,
                                                    melhor_valor,
                                                    tamanho_populacao,
                                                    taxa_cruzamento,
                                                    taxa_mutacao,
                                                    taxa_elitismo)

                            # Armazenando o melhor resultado na lista de resultados
                            self.resultados.append((melhor_cromossomo,
                                                    melhor_valor,
                                                    tamanho_populacao,
                                                    taxa_cruzamento,
                                                    taxa_mutacao,
                                                    taxa_elitismo))
                barra_progresso.update(1)  # Atualize a barra de progresso em 1 unidade

            barra_progresso.colour = 'green'
            barra_progresso.set_description("COMPLETO")
            barra_progresso.set_postfix({"Status": "Completo"})
            barra_progresso.refresh()
            barra_progresso.close()

            print("\033[32mExperimento completo!\033[0m")
            print('\n-----------------------------\n')


    def run(self):
        # Executando os experimentos
        self.executar_experimentos()

        # Salvando os resultados                        
        self.salvar_resultados()

if __name__ == '__main__':

   Experimento(1).run()
    
