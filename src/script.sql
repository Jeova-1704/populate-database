CREATE TABLE clientes (
    id_cliente TEXT PRIMARY KEY,
    nome TEXT,
    email TEXT,
    telefone TEXT,
    cidade TEXT,
    idade TEXT
);

CREATE TABLE produtos (
    id_produto TEXT PRIMARY KEY,
    nome_produto TEXT,
    categoria TEXT,
    preco TEXT,
    estoque TEXT
);

CREATE TABLE pedidos (
    id_pedido TEXT PRIMARY KEY,
    id_cliente TEXT REFERENCES clientes(id_cliente),
    id_produto TEXT REFERENCES produtos(id_produto),
    quantidade TEXT,
    status TEXT,
    valor_total TEXT,
    data_pedido TEXT
);