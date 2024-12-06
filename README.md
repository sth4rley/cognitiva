## 🚀 Instalação e Configuração

Siga os passos abaixo para configurar o ambiente e iniciar o servidor:

### 1. Clone o repositório:
```bash
git clone https://github.com/sth4rley/cognitiva.git
```

### 2. Acesse o diretório do projeto:
```bash
cd cognitiva
```

### 3. Configure o arquivo `.env`:
Crie o arquivo `.env` no diretório principal e adicione a sua chave de API:
```
API_KEY=CHAVEDAAPI
```

### 4. Crie e ative o ambiente virtual:
- **Linux/macOS**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

- **Windows**:
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

### 5. Instale as dependências:
```bash
pip install -r requirements.txt
```

### 6. Prepare o banco de dados:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Inicie o servidor local:
```bash
python manage.py runserver
```

### 8. Acesse a aplicação no navegador:
Abra [http://127.0.0.1:8000/](http://127.0.0.1:8000/) no navegador para acessar a plataforma.

---

## 🌐 Rotas Disponíveis

### **Principal**
- `/` – Página inicial da plataforma.

### **Salas de Aula**
- `/classrooms/` – Listagem de salas de aula.
- `/classrooms/add/` – Adicionar uma nova sala de aula.

### **Estudantes**
- `/students/` – Listagem de estudantes.
- `/students/add/` – Adicionar um novo estudante.
- `/students/<int:student_id>/difficulties/add/` – Registrar dificuldades para um estudante.
- `/students/<int:id>/report/` – Gerar relatório individual do estudante.

### **Professores**
- `/teachers/` – Listagem de professores.
- `/teachers/add/` – Adicionar um novo professor.

### **Conteúdo**
- `/content/` – Listagem de conteúdos.
- `/content/add/` – Adicionar novos conteúdos.

### **Dificuldades**
- `/edit_difficulty/<int:id>/` – Editar dificuldades registradas.

### **Administração**
- `/admin/` – Acesso ao painel administrativo.

---
