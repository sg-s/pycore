
.PHONY:  test coverage-report test-pip jupyter docs live-docs



live-docs: 
	@poetry run mkdocs serve -a 0.0.0.0:8000

docs: 
	@poetry run mkdocs build

test:
	@echo "Running tests with coverage..."
	@poetry run coverage run -m pytest -sx 

.coverage: 
	@poetry run coverage run --omit="*/test*" -m pytest -sx 

coverage-report: .coverage
	poetry run coverage html --omit="*/test*"
	open htmlcov/index.html


test-pip:
	@echo "Running tests for code installed with pip:"
	@coverage run -m pytest -sx 

jupyter:
	@echo "Installing kernel <pycore> in jupyter"
	-yes | jupyter kernelspec uninstall pycore
	poetry run python -m ipykernel install --user --name pycore
