# URL Shortener

Uma API escalável para encurtar URLs com cache distribuído, desenvolvida com FastAPI e arquitetura assíncrona para alto desempenho.

## Tech Stack

- **Framework Web**: FastAPI
- **Banco de Dados**: PostgreSQL
- **Cache**: Redis
- **Container**: Docker Compose
- **ORM/Query**: SQLAlchemy
- **Testes**: Pytest

## Instalação Local

1. **Clone o repositório**
   ```bash
   git clone https://github.com/ma-alves/url-shortener.git
   ```

2. **Configure as variáveis de ambiente**
   ```bash
   cp .env.example .env
   ```
   Edite o arquivo `.env` com as configurações necessárias.

3. **Inicie os serviços com Docker Compose**
   ```bash
   docker compose up --build
   ```
   Este comando irá:
   - Criar e iniciar o banco de dados
   - Iniciar o cache Redis
   - Executar as migrações do banco de dados
   - Iniciar a aplicação na porta 8000

4. **Verifique se a aplicação está rodando**
   ```bash
   curl http://localhost:8000/
   ```

5. **Acesse a documentação interativa**
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

### Parar os serviços

```bash
docker compose down
```

## API Endpoints

### 1. Página Inicial
- **Método**: `GET`
- **Rota**: `/`
- **Descrição**: Retorna mensagem de boas-vindas com link para documentação
- **Resposta (200)**:
  ```json
  {
    "message": "http://127.0.0.1:8000/docs#/"
  }
  ```

### 2. Encurtar URL
- **Método**: `POST`
- **Rota**: `/shorten`
- **Descrição**: Cria uma URL encurtada a partir de uma URL longa
- **Parâmetros**:
  - `url` (query, obrigatório): A URL a ser encurtada (formato HttpUrl)
- **Resposta (201)**:
  ```json
  {
    "uuid": "550e8400-e29b-41d4-a716-446655440000",
    "long_url": "https://exemplo.com/pagina-muito-longa",
    "short_code": "abc123",
    "created_at": "2026-01-29T10:30:00"
  }
  ```
- **Comportamento**: Se a URL já tiver sido encurtada anteriormente, retorna o código encurtado existente

### 3. Redirecionar para URL Original
- **Método**: `GET`
- **Rota**: `/{short_code}`
- **Descrição**: Redireciona para a URL original usando o código encurtado
- **Parâmetros**:
  - `short_code` (path, obrigatório): O código encurtado da URL
- **Resposta (302)**: Redireciona para a URL original
- **Resposta de Erro (404)**:
  ```json
  {
    "detail": "URL não encontrada."
  }
  ```
- **Cache**: As URLs acessadas são armazenadas em cache para melhor desempenho
