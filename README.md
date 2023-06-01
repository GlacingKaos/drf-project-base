# BASE - API REST

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
