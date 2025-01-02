"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel


def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """

    return

import pandas as pd
import zipfile
import os

def clean_campaign_data():
    input_folder = 'files/input/'
    output_folder = 'files/output/'


    os.makedirs(output_folder, exist_ok=True)


    client_df = pd.DataFrame(columns=['client_id', 'age', 'job', 'marital', 'education', 'credit_default', 'mortgage'])
    campaign_df = pd.DataFrame(columns=['client_id', 'number_contacts', 'contact_duration', 'previous_campaign_contacts', 'previous_outcome', 'campaign_outcome', 'last_contact_date'])
    economics_df = pd.DataFrame(columns=['client_id', 'cons_price_idx', 'euribor_three_months'])

    for file_name in os.listdir(input_folder):
        if file_name.endswith('.zip'):
            with zipfile.ZipFile(os.path.join(input_folder, file_name), 'r') as zip_ref:
                for csv_file in zip_ref.namelist():
                    with zip_ref.open(csv_file) as f:
                        df = pd.read_csv(f)
                        
                        data_client = df[['client_id', 'age', 'job', 'marital', 'education', 'credit_default', 'mortgage']].copy()
                        data_client['job'] = data_client['job'].str.replace('.', '').str.replace('-', '_')
                        data_client['education'] = data_client['education'].str.replace('.', '_').replace('unknown', pd.NA)
                        data_client['credit_default'] = data_client['credit_default'].apply(lambda x: 1 if x == 'yes' else 0)
                        data_client['mortgage'] = data_client['mortgage'].apply(lambda x: 1 if x == 'yes' else 0)
                        client_df = pd.concat([client_df, data_client], ignore_index=True)
                        
                        data_campaign = df[['client_id', 'number_contacts', 'contact_duration', 'previous_campaign_contacts', 'previous_outcome', 'campaign_outcome', 'day', 'month']].copy()
                        data_campaign['previous_outcome'] = data_campaign['previous_outcome'].apply(lambda x: 1 if x == 'success' else 0)
                        data_campaign['campaign_outcome'] = data_campaign['campaign_outcome'].apply(lambda x: 1 if x == 'yes' else 0)
                        meses = {'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6, 'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}
                        data_campaign['month'] = data_campaign['month'].map(meses)
                        data_campaign['last_contact_date'] = pd.to_datetime(data_campaign[['day', 'month']].assign(year=2022).rename(columns={'day': 'day', 'month': 'month'}))
                        data_campaign.drop(columns=['month', 'day'], inplace=True)
                        campaign_df = pd.concat([campaign_df, data_campaign], ignore_index=True)
                        
                        data_economics = df[['client_id', 'cons_price_idx', 'euribor_three_months']].copy()
                        economics_df = pd.concat([economics_df, data_economics], ignore_index=True)
    client_df.to_csv(os.path.join(output_folder, 'client.csv'), index=False)
    campaign_df.to_csv(os.path.join(output_folder, 'campaign.csv'), index=False)
    economics_df.to_csv(os.path.join(output_folder, 'economics.csv'), index=False)

if __name__ == "__main__":
    clean_campaign_data()
