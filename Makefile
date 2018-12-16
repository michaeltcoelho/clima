
.PHONY: install
install:
	@pip install .

.PHONY: local
development:
	@pip install -e ".[testing]"
