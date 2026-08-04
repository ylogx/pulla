VERSION = $(shell grep -m1 '^version' pyproject.toml | grep -o "[0-9]\+\.[0-9]\+\.[0-9]\+")
PYPIRC_TOKEN = python3 -c "import configparser,os; c=configparser.ConfigParser(); c.read(os.path.expanduser('~/.pypirc')); print(c['$(1)']['password'])"

.PHONY: test install build coverage clean publish test-publish

test:
	uv run pytest

install: build
	@echo "Installing pulla $(VERSION) with uv tool"
	uv tool install --force dist/pulla-$(VERSION)-py3-none-any.whl

build:
	@echo "Building distribution package for version $(VERSION)"
	uv build

coverage:
	uv run coverage run -m pytest
	uv run coverage report

clean:
	find . -type f -name '*.pyc' -exec rm {} +
	find . -type d -name '__pycache__' -exec rm -r {} +
	rm -rf dist build

publish: build
	@echo "Publishing pulla $(VERSION) to PyPI"
	UV_PUBLISH_TOKEN=$$($(call PYPIRC_TOKEN,pypi)) uv publish

test-publish: build
	@echo "Publishing pulla $(VERSION) to TestPyPI"
	UV_PUBLISH_TOKEN=$$($(call PYPIRC_TOKEN,testpypi)) uv publish --publish-url https://test.pypi.org/legacy/
