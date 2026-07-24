.PHONY: build lab smoke test lint

build:
	docker compose build

lab:
	docker compose up --build

smoke:
	test "$$(docker compose run --rm jupyter pwd)" = "/work"
	docker compose run --rm jupyter python -c "import numpy, qinst_ozawa; print(numpy.__version__, qinst_ozawa.__version__)"
	docker compose run --rm jupyter jupyter lab --version

test:
	docker compose run --rm jupyter pytest

lint:
	docker compose run --rm jupyter ruff check .
