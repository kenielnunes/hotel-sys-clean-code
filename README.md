# Ative o ambiente virtual
python3 -m venv venv
source venv/bin/activate  # ou .\venv\Scripts\activate no Windows

# Criar Requirements.txt com as libs
black
flake8
mypy
pytest
coverage

# Instale as dependências
pip install -r requirements.txt

# Rodar ferramentas
black app tests utils
flake8 app tests utils
mypy app tests utils
pytest

# Criar o banco de dados

python3 -m app.core.infra.config.database

# Rodar o App

PYTHONPATH=app python3 app/main.py