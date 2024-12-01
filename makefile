build:
	python -m build

clean-venv:
	rm -rf .venv

clean-dist:
	rm -rf dist

clean:
	$(MAKE) clean-venv
	$(MAKE) clean-dist

venv:
	$(MAKE) clean-venv
	python -m venv .venv && . .venv/scripts/activate

install:
	$(MAKE) clean-dist
	$(MAKE) build
	$(MAKE) venv && pip install dist/*.whl


