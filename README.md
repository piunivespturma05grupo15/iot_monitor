# Projeto Integrador - Grupo 15 - Turma 05 (UNIVESP)

Este é o repositório do Projeto Integrador do Grupo 15 da Turma 05 da UNIVESP. O sistema foi desenvolvido em Django e utiliza o banco de dados MySQL (via Docker) por padrão.

## 🛠️ Requisitos

- Python 3.10+ instalado  
- Git instalado  
- Docker instalado  

## 🚀 Como rodar o projeto localmente

### 1. Clone o repositório

```bash
git clone https://github.com/piunivespturma05grupo15/PI.git
cd PI
```

### 2. (Opcional) Crie um ambiente virtual

Recomendado para manter as dependências isoladas.

```bash
python -m venv venv
source venv/bin/activate  # no Windows use: venv\Scripts\activate
```

### 3. Instale as dependências do projeto

```bash
pip install -r requirements.txt
```

### 4. Suba o banco de dados MySQL com Docker

Certifique-se de que o Docker está instalado e rodando.

Execute o seguinte comando para criar e iniciar o container MySQL:

```bash
docker run --name mysql-dev \
  -e MYSQL_ROOT_PASSWORD=005Grupo-015 \
  -e MYSQL_DATABASE=monitoramentoprojetounivesp \
  -p 3306:3306 \
  -d mysql:8
```

> Obs: Este container cria um banco de dados chamado `monitoramentoprojetounivesp` com senha de root `005Grupo-015`. Verifique se as configurações estão corretas em seu `settings.py`.

### 5. Configure as variáveis de ambiente

Crie um arquivo `.env` (ou configure diretamente no `settings.py`) com as credenciais corretas do banco, por exemplo:

```env
DB_NAME=monitoramentoprojetounivesp
DB_USER=root
DB_PASSWORD=005Grupo-015
DB_HOST=localhost
DB_PORT=3306
```

### 6. Rode as migrações

```bash
python manage.py migrate
```

### 7. Inicie o servidor de desenvolvimento

```bash
python manage.py runserver
```

O servidor estará disponível em: [http://localhost:8000](http://localhost:8000)

---

## 📁 Estrutura do Projeto

```
PI/
├── Api/			#Django App
│
├── Projeto/		#Django Project
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── Projetos/        # Django App
│
├── manage.py
├── requirements.txt
└── README.md
```

---

## ✉️ Contato

Para dúvidas ou sugestões, entre em contato com um dos integrantes do grupo pelo GitHub.

---

**Desenvolvido com ❤️ por alunos da UNIVESP**