from tqdm import tqdm
import time

def loading_bar(mensagem='Carregando', colour='red', print_text='- loading pretrained model -'):
    print('\n')
    print(print_text)
    # Número total de itens a serem carregados
    total_itens = 100

    # Inicialize a barra de progresso com 0% (azul)
    barra_progresso = tqdm(total=total_itens, desc=mensagem, bar_format="{desc}: {percentage:3.0f}% {bar}", colour=colour)

    # Simule o carregamento de dados
    for i in range(total_itens):
        # Simule o carregamento de um item
        time.sleep(0.023)  # Simule uma carga de dados
        barra_progresso.update(1)  # Atualize a barra de progresso em 1 unidade

    # Carregamento completo, altere a barra para verde e exiba a mensagem
    barra_progresso.colour = 'green'
    barra_progresso.set_description("COMPLETO")
    barra_progresso.set_postfix({"Status": "Completo"})
    barra_progresso.refresh()
    barra_progresso.close()

    print("\033[32mCompleto!\033[0m")
