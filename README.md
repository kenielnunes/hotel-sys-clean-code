# Ative o ambiente virtual
python -m venv venv
source venv/bin/activate  # ou .\venv\Scripts\activate no Windows

# Instale as dependências
pip install -r requirements.txt

# Rodar ferramentas
black app tests utils
flake8 app tests utils
mypy app tests utils
pytest
