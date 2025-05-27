# Hotel System - Clean Code Refactor

## 📝 Descrição do Software

Este projeto é um sistema de gerenciamento de reservas para hotéis. Ele permite o cadastro de hóspedes, reserva de quartos, controle de estadias e check-out. O sistema foi refatorado com foco em **Clean Code**, **design modular** e aplicação de boas práticas de engenharia de software.

## ⚙️ Principais Funcionalidades

- Cadastro e busca de hóspedes  
- Reserva e liberação de quartos  
- Cálculo de diárias  
- Registro de histórico de reservas  
- Persistência em arquivos  
- Estrutura modularizada por responsabilidade (MVC)

## 🐞 Análise dos Principais Problemas Detectados

Durante a análise do código original, foram identificados os seguintes problemas:

- Código monolítico concentrado em um único arquivo (`projetofinal.py`)  
- Funções com múltiplas responsabilidades (violação do SRP)  
- Nomeclaturas genéricas e pouco descritivas  
- Baixa testabilidade devido ao acoplamento excessivo  
- Ausência de testes automatizados  
- Ausência de tipagem e validação estática  
- Duplicação de código  
- Persistência acoplada diretamente à lógica de negócios  

## 🛠️ Estratégia de Refatoração

A refatoração seguiu os princípios do **Clean Code**, visando:

- Separação de responsabilidades (uso de camadas: controllers, services, models, repositories)  
- Modularização do código em múltiplos arquivos e diretórios  
- Nomeclaturas significativas  
- Extração de métodos para reduzir complexidade  
- Aplicação de Interface Fluente em entidades (ex: padrão builder para facilitar encadeamento)  
- Cobertura de testes com `pytest`  
- Uso de `flake8`, `black`, `mypy` para garantir qualidade e padronização  

## 📜 ChangeLog (Resumo das Mudanças)

### [1.0.0] - Refatoração Inicial
- Separação de responsabilidades em camadas:
  - `controllers`, `services`, `models`, `repositories`, `utils`
- Entidades renomeadas e reorganizadas com tipagem
- Implementação da Interface Fluente (`Hospede`, `Reserva`)
- Persistência desacoplada usando classes de repositório
- Adição de testes unitários com `pytest`
- Padronização com `black`, `flake8`, `mypy`
- Estrutura de diretórios limpa e orientada a domínio
- Substituição de prints por retornos claros e reutilizáveis
- Implementação de fábrica de objetos (ex: `HospedeFactory`)
- Interface de entrada extraída para modularidade
- Organização do menu principal em um controlador

## ✅ Testes Implementados

- Testes unitários com `pytest`  
- Testes de serviços e casos de uso  
- Cobertura dos principais fluxos de reserva e cadastro  
- Estrutura em diretório `tests/`  
- Validação de entrada, simulação de reservas e liberação de quartos  
- Execução via `pytest`

## 🔄 Interface Fluente

Foi implementado o padrão de **Interface Fluente** (Fluent Interface) especialmente nos objetos de domínio. Por exemplo:

`python`
hospede = Hospede().com_nome("João").com_documento("123456").com_idade(30)


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

# Rodar o Sonarqube

sonar-scanner
