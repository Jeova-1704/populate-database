
# Gerador de Dados para Banco de Dados no Supabase

### Descrição do Projeto
Este projeto tem como objetivo popular um banco de dados no Supabase com dados sintéticos que contêm valores corretos, valores errados e valores ausentes. Isso permite a imersão e experimentação com processos de Extração, Transformação e Carregamento de dados (ETL), bem como pipelines de dados.

### Tecnologias Utilizadas

- Python - Linguagem principal do projeto
- Supabase - Banco de dados utilizado para armazenar os dados gerados
- Faker - Biblioteca para geração de dados fictícios
- Pandas - Para manipulação e estruturação dos dados
- Dotenv - Para gerenciar variáveis de ambiente

### Estrutura do Projeto

```bash

├── src/
│   ├── connection.py  # Gerencia a conexão com o Supabase
│   ├── generated_data.py  # Gera e insere os dados no banco
│   ├── main.py  # Arquivo principal para execução do script
│   ├── script.sql  # Script para criação das tabelas no Supabase
│   ├── utils.py  # Contém listas de categorias, status e erros de dados
├── .env.example  # Exemplo de arquivo de variáveis de ambiente
├── .gitignore  # Arquivo de exclusão de arquivos sensíveis no repositório
├── README.md  # Documentação do projeto
├── requirements.txt  # Dependências do projeto
```

### Configuração e Execução
Clonar o Repositório
```bash
git clone <URL_DO_REPOSITORIO>
cd <NOME_DO_REPOSITORIO>
```

### Criar e Ativar um Ambiente Virtual
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate  # Windows
```

### Instalar Dependências
```bash
pip install -r requirements.txt
```

### Configurar Variáveis de Ambiente

Copie o arquivo .env.example, renomeie para .env e preencha os valores:

```python
SUPABASE_URL="sua_url_do_supabase"
SUPABASE_KEY="sua_chave_do_supabase"
```

### Criar as Tabelas no Supabase
Execute o script SQL no painel do Supabase:
```sql
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
```
Executar o Script

### Para gerar e popular os dados no Supabase:
```bash
python src/main.py
```

### Funcionamento
O script generated_data.py gera 100.000 registros para cada tabela (clientes, produtos e pedidos), introduzindo erros propositalmente em nomes e e-mails, valores nulos e dados incorretos. O main.py chama essa função em um loop para inserir dados continuamente no banco.
