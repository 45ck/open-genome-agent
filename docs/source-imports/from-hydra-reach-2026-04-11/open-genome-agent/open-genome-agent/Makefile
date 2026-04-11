.PHONY: build test clean zip

build:
	python scripts/build_all.py

test:
	python -m unittest discover -s tests -p "test_*.py"

clean:
	find . -name "__pycache__" -type d -prune -exec rm -rf {} +
	find . -name "*.pyc" -delete

zip:
	cd .. && zip -r open-genome-agent.zip open-genome-agent
