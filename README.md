## How to run project

1. Clone project with git
2. Move to project root folder with `cd emailClient`
3. Create virtal enviroment with `python -m venv venv`
4. Active virtual enviroment with `source venv/bin/activate` (in Windows `venv\Scripts\activate`)
5. Install proyect's packages with `pip install -r requirements.txt`
6. If you have Docker, you can run `docker run --name email_db -e POSTGRES_PASSWORD=yoursecretpass -p 5432:5432 --rm -d postgres` to run your Postgres database server
7. In your db server, create a database named `email_db` (it's depends of databases name in [settings.py](./mail_app_be/settings.py) file, line 86)
8. If you are on windows `pip install django-extensions`
9. Once you have your db, you can run migrations with 
    ```python
    python manage.py makemigrations
    python manage.py migrate
    ```
10. Finally you can run th server with `python manage.py runserver`
