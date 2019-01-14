init:
	python -m venv venv; \
	echo 'source venv/bin/activate' >> .env; \
	echo 'export DATABASE_URL=""' >> .env; \
	echo 'export REDIS_URL=""' >> .env; \
	source ./venv/Scripts/Activate; \
	pip install -r requirements.txt; \

run:
	python manage.py run

update_deps:
	source ./venv/bin/activate; \
	pip install --upgrade -r requirements.txt; \

revision:
	PYTHONPATH=./src alembic revision --autogenerate;

upgrade:
	PYTHONPATH=./src alembic upgrade head

downgrade:
	PYTHONPATH=./src alembic downgrade head