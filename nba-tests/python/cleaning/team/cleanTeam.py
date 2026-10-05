import json


def ordenate():
    """
    Lê um arquivo JSON, organiza os dados por nome de equipe,
    reindexa os itens e salva em um novo arquivo.
    """

    # Lê o arquivo JSON, tratando cada linha como um objeto JSON separado
    with open('../../scrape/team/json/2026.json', 'r') as file:
        data_list = [json.loads(line) for line in file]

    # Organiza a lista de times em ordem alfabética usando a chave 'Team'
    sorted_data = sorted(data_list, key=lambda x: x['Team'])

    # Reindexa os itens de 1 a N
    for i, team in enumerate(sorted_data):
        team['index'] = i + 1

    # Cria uma nova estrutura de dicionário com a chave 'teams'
    output_data = {"teams": sorted_data}

    # Salva o resultado em um novo arquivo JSON
    with open('2026_sorted.json', 'w') as f:
        json.dump(output_data, f, indent=4)


# Exemplo de como usar a função com os arquivos que você forneceu:
if __name__ == "__main__":
    ordenate()
