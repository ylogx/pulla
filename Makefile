PACKAGE="Pulla"
PACKAGE_LOWER=$(shell echo $(PACKAGE) | sed 's/.*/\L&/')
PIP_EXEC=pip
PYTHON_EXEC=python3
PYTHON2_EXEC=python2.7
PYTHON3_EXEC=python3
NOSETESTS_EXEC=$(shell which nosetests)
VERSION = $(shell grep -o "[0-9]\+\.[0-9]\+\.[0-9]\+" setup.py)
TEST_FILES = $(wildcard tests/test_*.py)
TESTS = $(subst .py,,$(subst /,.,$(TEST_FILES)))

all.PHONY: nosetests_3 nosetests_2

nosetests_2:
	@echo "Running $(PYTHON2_EXEC) tests"
	@$(PYTHON2_EXEC) $(NOSETESTS_EXEC)

nosetests_3:
	@echo "Running $(PYTHON3_EXEC) tests"
	@$(PYTHON3_EXEC) $(NOSETESTS_EXEC)

install:
	@echo "Creating distribution package for version $(VERSION)"
	@echo "-----------------------------------------------"
	$(PYTHON_EXEC) setup.py sdist
	@echo "Installing package using $(PIP_EXEC)"
	@echo "----------------------------"
	$(PIP_EXEC) install --upgrade dist/$(PACKAGE)-$(VERSION).tar.gz

coverage:
	@coverage run $(NOSETESTS_EXEC)
	@coverage report

rst_test:
	pandoc --from=markdown --to=rst README.md | rst2html.py >/dev/null

clean:
	find . -type f -name '*.pyc' -exec rm {} +
	find . -type d -name '__pycache__' -exec rm -r {} +
