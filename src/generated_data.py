import pandas as pd
from faker import Faker
import random
from connection import Connection
from os import getenv
from utils import CATEGORIAS_PRODUTOS, STATUS_PEDIDO, ERROS_NOMES, ERROS_EMAIL

fake = Faker()
num_registros = 10_000

categorias_produto = CATEGORIAS_PRODUTOS
status_pedido = STATUS_PEDIDO
erros_nome = ERROS_NOMES
erros_email = ERROS_EMAIL


def random_nullable(value):
    """ Retorna o valor original ou NULL/"" com 20% de chance. """
    return value if random.random() > 0.2 else random.choice(["", None])


def generate_data():
    clientes = []
    produtos = []
    pedidos = []

    for _ in range(num_registros):
        id_cliente = str(fake.uuid4())
        cliente = {
            "id_cliente": id_cliente,
            "nome": random_nullable(random.choice(erros_nome) if random.random() < 0.02 else fake.name()),
            "email": random_nullable(random.choice(erros_email) if random.random() < 0.02 else fake.email()),
            "telefone": random_nullable(fake.phone_number()),
            "cidade": random_nullable(fake.city()),
            "idade": random_nullable(str(fake.random_int(min=18, max=80)))
        }
        clientes.append(cliente)

    for _ in range(num_registros):
        id_produto = str(fake.uuid4())
        produto = {
            "id_produto": id_produto,
            "nome_produto": random_nullable(fake.word() + " " + random.choice(categorias_produto)),
            "categoria": random_nullable(random.choice(categorias_produto)),
            "preco": random_nullable(str(round(random.uniform(5, 5000), 2))),
            "estoque": random_nullable(str(random.randint(0, 500)))
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
            "quantidade": random_nullable(str(random.randint(1, 10))),
            "status": random_nullable(random.choice(status_pedido)),
            "valor_total": random_nullable(str(round(random.uniform(10, 5000), 2))),
            "data_pedido": random_nullable(str(fake.date_between(start_date='-2y', end_date='today')))
        }
        pedidos.append(pedido)

    return clientes, produtos, pedidos


def list_to_df():
    clientes, produtos, pedidos = generate_data()
    df_clientes = pd.DataFrame(clientes)
    df_produtos = pd.DataFrame(produtos)
    df_pedidos = pd.DataFrame(pedidos)

    return df_clientes, df_produtos, df_pedidos


def insert_data():
    try:
        url = getenv("SUPABASE_URL")
        key = getenv("SUPABASE_KEY")
        connection = Connection(url, key)
        client = connection.get_client()

        df_clientes, df_produtos, df_pedidos = list_to_df()


        df_clientes = df_clientes.where(pd.notna(df_clientes), None)
        df_produtos = df_produtos.where(pd.notna(df_produtos), None)
        df_pedidos = df_pedidos.where(pd.notna(df_pedidos), None)


        client.table('clientes').insert(df_clientes.to_dict(orient='records')).execute()
        client.table('produtos').insert(df_produtos.to_dict(orient='records')).execute()
        client.table('pedidos').insert(df_pedidos.to_dict(orient='records')).execute()

        print("Data inserted successfully!")
        connection.close()
    except Exception as e:
        print(f"Error inserting data: {e}")
        connection.close()
        raise e
    