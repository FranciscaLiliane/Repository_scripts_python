import requests
from requests.auth import HTTPBasicAuth
import csv

# Parâmetros de autenticação
organization_name = ""
personal_access_token = ""

organization_url = f"https://vsaex.dev.azure.com/{organization_name}/_apis/userentitlements?top=1000&api-version=7.1-preview.1"  

# Realiza a chamada à API com autenticação usando o Personal Access Token
response = requests.get(organization_url, auth=HTTPBasicAuth("", personal_access_token))

# Verifique se a chamada à API foi bem-sucedida
if response.status_code == 200:
    data = response.json()

    # Inicialize uma lista para armazenar os dados
    data_list = []

    for member in data["value"]:
        licenca = member["accessLevel"]["licenseDisplayName"]

        data_list.append({
            "Nome": member["user"]["displayName"],
            "Licenca": licenca,
        })

    # Nome do arquivo CSV de saída
    csv_filename = "relatorio.csv"

    # Escreva os dados em um arquivo CSV
    with open(csv_filename, mode="w", newline="") as csv_file:
        fieldnames = ["Nome", "Licenca"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for row in data_list:
            writer.writerow(row)

    print(f"Relatório CSV gerado com sucesso em {csv_filename}.")
else:
    print("Erro ao listar usuários. Response:", response.status_code)
