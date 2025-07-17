install:
	pip install -r requirements.txt || pip install 'fastapi[all]' sqlalchemy alembic python-dotenv psycopg2-binary 'python-jose[cryptography]' 'passlib[bcrypt]'

run:
	uvicorn backend.main:app --reload

migrate:
	alembic upgrade head

makemigrations:
	alembic revision --autogenerate -m "manual migration" 

seed:
	python -m backend.seed 

test:
	PYTHONPATH=. pytest tests 

run-all:
	uvicorn backend.main:app --reload & streamlit run streamlit_app.py 

run-streamlit:
	streamlit run streamlit_app.py 