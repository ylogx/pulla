TEST_FILES = $(wildcard tests/test_*.py)
TESTS = $(subst .py,,$(subst /,.,$(TEST_FILES)))
VERSION = 0.0.6

all.PHONY: nosetests_2_3

nosetests_2_3:
	@echo "Running python2 tests"
	@python2.7 `which nosetests`
	@echo "Running python3 tests"
	@python3 `which nosetests`

install:
	@echo "Creating distribution package for version $(VERSION)"
	@echo "-----------------------------------------------"
	python3 setup.py sdist
	@echo "Installing package using pip"
	@echo "----------------------------"
	sudo pip install --upgrade dist/Pulla-$(VERSION).tar.gz

test:
	@- $(foreach TEST,$(TESTS), \
		echo === Running test: $(TEST); \
		python -m $(TEST) $(PYFLAGS); \
		)

test2:
	@- $(foreach TEST,$(TESTS), \
		echo === Running python2 test: $(TEST); \
		python2 -m $(TEST) $(PYFLAGS); \
		)
test3:
	@- $(foreach TEST,$(TESTS), \
		echo === Running python3 test: $(TEST); \
		python3 -m $(TEST) $(PYFLAGS); \
		)
