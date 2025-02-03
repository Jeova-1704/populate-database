import pandas as pd
from faker import Faker
import random
from connection import Connection
from os import getenv
from utils import CATEGORIAS_PRODUTOS, STATUS_PEDIDO
from dotenv import load_dotenv

fake = Faker()
num_registros = 10_000

categorias_produto = CATEGORIAS_PRODUTOS
status_pedido = STATUS_PEDIDO

def generate_data():
    clientes = []
    produtos = []
    pedidos = []

    for _ in range(num_registros):
        id_cliente = str(fake.uuid4())
        cliente = {
            "id_cliente": id_cliente,
            "nome": fake.name(),
            "email": fake.email(),
            "telefone": fake.phone_number(),
            "cidade": fake.city(),
            "idade": str(fake.random_int(min=18, max=80))
        }
        clientes.append(cliente)

    for _ in range(num_registros):
        id_produto = str(fake.uuid4())
        produto = {
            "id_produto": id_produto,
            "nome_produto": (fake.word() + " " + random.choice(categorias_produto)),
            "categoria": random.choice(categorias_produto),
            "preco": str(round(random.uniform(5, 5000), 2)),
            "estoque": str(random.randint(0, 500))
        }
        produtos.append(produto)

    for _ in range(num_registros):
        id_pedido = str(fake.uuid4())
        cliente_escolhido = random.choice(clientes)
        produto_escolhido = random.choice(produtos)
        
        pedido = {
            "id_pedido": id_pedido,
            "id_cliente": cliente_escolhido["id_cliente"],
            "id_produto": produto_escolhido["id_produto"],
            "quantidade": str(random.randint(1, 10)),
            "status": random.choice(status_pedido),
            "valor_total": str(round(random.uniform(10, 5000), 2)),
            "data_pedido": str(fake.date_between(start_date='-2y', end_date='today'))
        }
        pedidos.append(pedido)

    return clientes, produtos, pedidos


def list_to_df():
    print("Generating data...")
    clientes, produtos, pedidos = generate_data()
    df_clientes = pd.DataFrame(clientes)
    print("Data generated for clients...")
    df_produtos = pd.DataFrame(produtos)
    print("Data generated for products...")
    df_pedidos = pd.DataFrame(pedidos)
    print("Data generated for orders...")

    return df_clientes, df_produtos, df_pedidos


def insert_data():
    try:
        load_dotenv()
        url = getenv("SUPABASE_URL")
        key = getenv("SUPABASE_KEY")
        connection = Connection(url, key)
        client = connection.get_connection()
        print("Connection established!")

        df_clientes, df_produtos, df_pedidos = list_to_df()
        

        client.table('clientes').insert(df_clientes.to_dict(orient='records')).execute()
        print("Data inserted for clients...")
        client.table('produtos').insert(df_produtos.to_dict(orient='records')).execute()
        print("Data inserted for products...")
        client.table('pedidos').insert(df_pedidos.to_dict(orient='records')).execute()
        print("Data inserted for orders...")

        print("Data inserted successfully!")
    except Exception as e:
        print(f"Error inserting data: {e}")
        raise e
    finally:
        connection.close_connection()
    