# Sugarcane Disease Predictor API 🌿🌾

API RESTful para identificação e classificação de doenças em folhas de cana-de-açúcar através de Visão Computacional e Deep Learning, utilizando um modelo treinado com **MobileNetV3**.

---

## 📋 Sumário
- [Sobre o Projeto](#-sobre-o-projeto)
- [Classes Suportadas](#-classes-suportadas)
- [Arquitetura e Tecnologias](#-arquitetura-e-tecnologias)
- [Estrutura do Repositório](#-estrutura-do-repositório)
- [Requisitos Prévios](#-requisitos-prévios)
- [Instalação e Uso](#-instalação-e-uso)
  - [Executando com Docker Compose](#-executando-com-docker-compose)
  - [Executando Localmente com Poetry](#-executando-localmente-com-poetry)
- [Endpoints da API](#-endpoints-da-api)
- [Executando os Testes](#-executando-os-testes)
- [Versionamento de Dados (DVC)](#-versionamento-de-dados-dvc)

---

## 🔬 Sobre o Projeto

Este repositório contém o modelo de aprendizado profundo (`sugarcane_model_v1.keras`), o notebook de treinamento/fine-tuning (`diseases_predictor_in_sugarcane.ipynb`) e a API construída com **FastAPI** para servir inferências em tempo real a partir do envio de imagens de folhas de cana-de-açúcar.

---

## 🏷️ Classes Suportadas

O modelo é capaz de classificar 5 categorias:

1. **`Healthy`** (Saudável)
2. **`Mosaic`** (Mosaico)
3. **`RedRot`** (Podridão Vermelha)
4. **`Rust`** (Ferrugem)
5. **`Yellow`** (Amarelamento / Yellow Leaf)

---

## 🛠️ Arquitetura e Tecnologias

- **FastAPI**: Framework web moderno e assíncrono em Python.
- **Keras / TensorFlow**: Carregamento e inferência do modelo `MobileNetV3`.
- **Pillow & NumPy**: Processamento e redimensionamento das imagens.
- **Poetry**: Gerenciamento de dependências e ambientes virtuais.
- **PostgreSQL / SQLAlchemy / Alembic**: Banco de dados e migrações.
- **Docker & Docker Compose**: Conteinerização da aplicação.
- **Pytest & HTTPX**: Testes unitários e de integração assíncronos.
- **DVC**: Versionamento do dataset de imagens.

---

## 📂 Estrutura do Repositório

```text
diseases-predictor-in-sugarcane/
├── api/                       # Código-fonte da API em FastAPI
│   ├── app/
│   │   ├── core/              # Configurações de ambiente
│   │   ├── db/                # Conexão e modelos do banco de dados
│   │   ├── endpoints.py       # Endpoint POST /predict para inferência
│   │   └── main.py            # Instância principal do FastAPI
│   ├── tests/                 # Testes unitários com pytest
│   ├── pyproject.toml         # Configuração do Poetry e dependências
│   └── poetry.lock            # Lockfile do Poetry
├── sugarcane_model_v1.keras   # Modelo Keras treinado (MobileNetV3)
├── diseases_predictor_in_sugarcane.ipynb # Notebook de treinamento
├── Dockerfile                 # Dockerfile da aplicação
├── docker-compose.yml         # Orquestração dos serviços (API + PostgreSQL)
├── Makefile                   # Comandos facilitadores para automação
└── README.md                  # Documentação do projeto
```

---

## ⚙️ Requisitos Prévios

- Python `^3.11` ou `^3.12`
- [Poetry](https://python-poetry.org/)
- [Docker](https://www.docker.com/) e [Docker Compose](https://docs.docker.com/compose/) (opcional, para ambiente conteinerizado)

---

## 🚀 Instalação e Uso

### ⚡ Inicialização Rápida com `make start` (Recomendado)

O projeto possui um **Makefile** configurado para automatizar todo o processo de inicialização (criação do `.env`, geração do `requirements.txt` via Poetry, build dos containers Docker e migração do banco de dados):

```bash
make start
```

---

### 🐳 Executando com Docker Compose Manualmente

Para subir a API integrada com o banco de dados PostgreSQL:

```bash
# 1. Copiar as variáveis de ambiente
cp api/config/.env-example .env

# 2. Subir os containers com Docker Compose
docker-compose up -d --build

# 3. Aplicar as migrações no banco
docker-compose run --rm apistartkit alembic upgrade head
```

A API estará acessível em: `http://localhost:8000`  
Documentação interativa Swagger: `http://localhost:8000/docs`

---

### 💻 Executando Localmente com Poetry

```bash
# 1. Navegar até o diretório da API
cd api

# 2. Instalar as dependências com o Poetry
poetry install

# 3. Executar o servidor de desenvolvimento
poetry run uvicorn app.main:app --reload --port 8000
```

---

## 📌 Endpoints da API

### `POST /predict/`
Envia uma imagem de folha de cana-de-açúcar para classificação.

- **Request**: `multipart/form-data` contendo a chave `file` com a imagem (`.jpg`, `.png`, etc.).
- **Response** (`200 OK`):

```json
{
  "class_name": "Healthy",
  "confidence": 0.9412,
  "probabilities": {
    "Healthy": 0.9412,
    "Mosaic": 0.0215,
    "RedRot": 0.0120,
    "Rust": 0.0153,
    "Yellow": 0.0100
  }
}
```

---

## 🧪 Executando os Testes

Para rodar os testes unitários e de integração:

```bash
cd api
ENVIRONMENT=test poetry run pytest
```

Ou via `Makefile` na raiz do projeto:

```bash
make test
```

---

## 🛠️ Atalhos com Makefile

O repositório disponibiliza um [Makefile](file:///home/kauan/projects/sugar_api/diseases-predictor-in-sugarcane/Makefile) com atalhos para os comandos mais comuns:

| Comando | Descrição |
| :--- | :--- |
| `make start` | Executa o setup (`.env`), gera o `requirements.txt`, sobe os containers e executa as migrações |
| `make test` | Executa a suíte de testes com `pytest` dentro do container Docker |
| `make create-requirements` | Exporta o `requirements.txt` atualizado a partir do Poetry |
| `make makemigrations` | Cria uma nova migração do Alembic no banco de dados |
| `make migrate` | Aplica as migrações pendentes no banco de dados |
| `make ruff-check` | Executa a verificação de linting do código com `ruff` |
| `make ruff-fix` | Corrige automaticamente problemas de código com `ruff` |
| `make coverage` | Executa os testes com relatório de cobertura de código |

---

## 📊 Versionamento de Dados (DVC)


O repositório utiliza **DVC** para rastrear o dataset de imagens de forma desacoplada do Git:

```bash
# Baixar ou atualizar datasets via DVC
dvc pull
```
