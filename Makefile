install:
	python -m pip install -r backend/requirements.txt

test:
	pytest -q

run:
	python -m backend.main