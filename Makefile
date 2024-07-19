.PHONY: install
install:
	python -m pip install --upgrade pip
	if [ -f requirements.txt ]; then pip install -r requirements.txt; fi

.PHONY: migrate
migrate:
	python -m manage migrate

.PHONY: migrations
migrations:
	python -m manage makemigrations

.PHONY: superuser
superuser:
	python -m manage createsuperuser
	
.PHONY: test
test:
	python -m manage test

.PHONY: run
run:
	python -m manage runserver


.PHONY: lint
lint:
	pre-commit run --all-files
