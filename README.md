# Desafio PD Hours Control
## Wesley Velloso Marques

Foi utilizado o framework Django com PostgreSQL, com a biblioteca psycopg2. Utiizei o Windows 10.

Executei o projeto django no VS Code, migrando o esquema para uma base de dados Postgre no pgadmin4. 

Rodei a aplicação localmente (127.0.0.1) na porta padrão 5432.

Requisitos: Python 3.10.0 e PostgreSQL 14 instalados na máquina, VS code e pgadmin4.

Criar uma database no pgadmin4: Botão direito em PostgreSQL 14 > Create > Database.

Nomear a database e o proprietário (Deixei o propietário 'postgres' padrão assim como as demais configurações padrão).

Execução do ambiente:

Clonar DjangoProjects do github e abrir no VS Code.

Abrir o arquivo settings.py no diretório PDHours

Na linha 77, substituir os dados para a database nova:

DATABASES = {

    'default': {

        'ENGINE': 'django.db.backends.postgresql_psycopg2',

        'NAME': 'HoursDb', 

        'USER': 'postgres', 

        'PASSWORD': '99861065',

        'HOST': '127.0.0.1',

        'PORT': '5432',
    }
}

Substituir HoursDb pelo nome da database criada. 

O Password utilizado é o mesmo que foi indicado no momento da instalação do PostgreSQL 14 na máquina.

Salvar o settings.py.

Abrir um terminal powershell no VS Code.

Ativar o ambiente:

cd env 

scripts/activate 

Aplicar as migrações para a database conectada:
cd PDHours 

python manage.py makemigrations

python manage.py migrate

python manage.py makemigrations HoursApp

python manage.py migrate HoursApp

A partir daqui, as tabelas Squad,User e Reports estarão na database.
Além delas, haverão outras tabelas criadas pelo Django, que servem para autenticação de usuário, grupos, permissões, etc.
São necessárias para, entre outras coisas, criar e verificar super usuário(s) e rodar o servidor localmente.

Popular database:

python manage.py loaddata db.json 

Rodar o servidor:

python manage.py createsuperuser

(Preencher os dados para criação de super usuário)

python manage.py runserver

Ctrl + click em http://127.0.0.1:8000/

No aba que abrirá no navegador, logar como super usuário.

Executar as queries através do arquivo queries.txt na raiz do projeto. 