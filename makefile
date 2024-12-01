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
	( \
		python -m venv .venv; \
		source .venv/scripts/activate; \
		pip install build; \
	)

install-build:
	pip install dist/*.whl

install:
	( \
		pip install --editable .; \
	)
    


