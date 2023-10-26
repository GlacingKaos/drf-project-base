# BASE - API REST with Django and DRF

## CREAR LOS ENVs
1. Crear el archivo `.env` en la raiz del proyecto
2. Copiar el contenido de `.env.example` al archivo `.env` creado en el paso 1
3. Modificar el `.env`, si ocupa modificar alguna config del entorno

## run api
```
docker compose up -d api_db
docker compose up -d api
```

## run migrations
```
docker compose exec api python3 manage.py migrate
```

## crear superuser
```
docker compose exec api python3 manage.py createsuperuser --email admin@example.com
```

## create migrations
```
docker compose exec api python3 manage.py makemigrations
```

## generate configs (Countrie, Language, Timezone)
```
docker compose exec api python3 manage.py generate_confis
```

## run tests
```
docker compose exec api python3 manage.py test
```

## Setup project with pyenv

1. Install [pyenv](https://github.com/pyenv/pyenv-installer#install). [Requirements of pyenv](https://github.com/pyenv/pyenv/wiki#suggested-build-environment) to compile Python versions
2. Once pyenv is installed is required to install the Python version that we are using

    ```jsx
    pyenv install 3.10.10
    ```

3. Now you have to create a new virtual environment for the Insights project running this command:
    ```jsx
    pyenv virtualenv  3.10.10 drfprojectbase
    cd YOUR_PROJECT_FOLDER
    echo drfprojectbase > .python-version
    ```

4. [Install poetry](https://python-poetry.org/docs/#installing-with-the-official-installer)
    ```jsx
    pip install poetry
    ```
5. cdRun `poetry install` to install all dependencies of the project. **NOTE:** You may present some errors during the installation of some libraries, by the end of this page you can find some resources to solve it

    ```jsx
    poetry install
    ```
