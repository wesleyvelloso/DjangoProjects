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
No aba que abrirá no navegador, logar como super usuário




Execução das querys no terminal da IDE (utilizado VS Code no Windows 10):
No terminal powershell, com o ambiente ativado:

python manage.py shell
from HoursApp.models import Squad,User,Report
from django.db.models import Sum
from datetime import date,timedelta

Query #1- Retorna as horas gastas de cada membro de uma determinada squad em um determinado período:

Pode ser copiado os blocos abaixo de uma só vez para o shell:

squad_name='Mobile Development'
initial_date = '2021-10-06'
final_date = '2021-10-30'
squad = User.objects.filter(squadid__name=squad_name)
interval = squad.filter(user_reports__created_at__range=[initial_date,final_date])
not_interval = squad.exclude(user_reports__created_at__range=[initial_date,final_date])
work_hours = interval.values('name').annotate(sum=Sum('user_reports__spent_hours'))
if not work_hours:
     print('[',squad_name,'][',initial_date,'to',final_date,'] -> No reports in the given period') 
else:
    for member in work_hours:
        print('[',squad_name,'][',initial_date,'to',final_date,'] ->',member['name'],'-> Work Hours = ',member['sum'])
        for member in not_interval:
            print('[',squad_name,'][',initial_date,'to',final_date,'] ->',member['name'],'-> Without reports in the given period')


teclar enter(2x)


Query #2 - Retorna o tempo total gasto de uma squad em um determinado período, ou seja, a quantidade total de horas realizadas pelos membros daquela squad:

squad_name='Hardware Development'
initial_date = '2021-11-12'
final_date = '2021-11-30'
squad = User.objects.filter(squadid__name=squad_name)
interval = squad.filter(user_reports__created_at__range=[initial_date,final_date])
if not interval:
    print('[',squad_name,'][',initial_date,'to',final_date,'] -> No reports in the given period')
else:
    squad_total_hours = interval.values('squadid').annotate(sum=Sum('user_reports__spent_hours'))
    for m in squad_total_hours:
        print('[',squad_name,'][',initial_date,'to',final_date,'] -> Total work hours = ',m['sum'])

teclar enter(2x)


Query #3- Retorna a média gasta de horas por dia de uma squad em um determinado período:

squad_name='Back-end development'
initial_date = date(2021, 11, 12)
final_date = date(2021, 11, 19)
squad = User.objects.filter(squadid__name=squad_name)
interval = squad.filter(user_reports__created_at__range=[initial_date,final_date])
if not interval:
    print('[',squad_name,'][',initial_date,'to',final_date,'] -> No reports in the given period')
else:
    period = (final_date - initial_date).days
    squad_total_hours = interval.values('squadid').annotate(sum=Sum('user_reports__spent_hours'))
    for m in squad_total_hours:
        avg_hours = m['sum']/period
        print('[',squad_name,'][',initial_date,'to',final_date,']-> Daily average of working hours = ',avg_hours)