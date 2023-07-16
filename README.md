# party.darklite.org

> You'll never travel alone.
> 
> Even if you'd want to.

***

Deployment:

1. copy `.env-example` to `.env` and change settings needed for deployment
2. copy `.db-env-example` to `.db-env` and change settings needed
3. copy `app/.env-example` to `app/.env` and change settings needed for the app
4.  `docker compose build`
5. `docker compose run --rm app python3 manage.py migrate` to initialize the db
6. `docker compose run --rm app python3 manage.py createsuperuser` to create the superuser
7. `docker compose run --rm app python3 manage.py collectstatic --no-input` to get static files in the correct places 
8. `docker compose up -d` to deploy to localhost:8000