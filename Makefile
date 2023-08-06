setup:
	python3.10 -m venv venv
	venv/Scripts/activate
	pip install -r backend/requirements-dev.txt
	pip install -r beckand/requirements.txt
	cd frontend
	npm install