run:
	uvicorn api.main:app --reload
streamlit:
	streamlit run app/app.py

run-all:
	$(MAKE) run &
	$(MAKE) streamlit 

test:
	python -m unittest discover -s tests

format:
	ruff check .
	ruff format .