## START DB ##

```
python3 -m pip install -r requirements.txt
```
```
docker compose up -d --build
```
```
python3 -m alembic upgrade head
```

## MIGRATE DB ##

```
python3 -m alembic revision --autogenerate
```
```
python3 -m alembic upgrade head
```