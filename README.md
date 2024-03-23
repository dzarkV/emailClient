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

## Improvements - Milestone 2: Maturing - backend

As code improvements for back-end from group 8 to group 9, we suggest:

- **Updating User Model:** By changing the primary key from email address to an auto-incremented ID, we enhance the system’s flexibility. Email addresses can change, which could lead to complications with foreign key relationships. An auto-incremented ID remains constant, providing a more stable reference point. Additionally, keeping the email as a unique field ensures that each user has a unique identifier beyond the primary key.
- **JWT Based Authentication**: Implementing JWT (JSON Web Tokens) based authentication provides a secure and scalable method for user authentication. JWTs are stateless, meaning the server does not need to store session data. This makes the system more scalable and reduces server load.
- **Use Django's built in functions for password checking/hashing**: Django’s make_password and authenticate abstract away the details of password hashing and checking (They handle the salting and hashing of passwords). This makes the code simpler and easier to read.
- **Protecting Views**: By requiring a bearer token in the auth headers for multiple endpoints, we ensure that only authenticated users can access these resources. Also updated the views to match the new primary key and to make use of the JWT to get user info.
- **Use Gunicorn in Production:** The built-in Django server is [not designed to be a production server.](https://docs.djangoproject.com/en/5.0/ref/django-admin/#runserver) It is a lightweight server meant for development. [Gunicorn](https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/gunicorn/), on the other hand, is a WSGI HTTP server that is designed for production use, offering robustness and efficient handling of multiple simultaneous requests.