TEST_FILES = $(wildcard tests/test_*.py)
TESTS = $(subst .py,,$(subst /,.,$(TEST_FILES)))

all.PHONY: test

test:
	@- $(foreach TEST,$(TESTS), \
		echo === Running test: $(TEST); \
		python -m $(TEST) $(PYFLAGS); \
		)

test26:
	@- $(foreach TEST,$(TESTS), \
		echo === Running python2.6 test: $(TEST); \
		python2.6 -m $(TEST) $(PYFLAGS); \
		)
test27:
	@- $(foreach TEST,$(TESTS), \
		echo === Running python2.7 test: $(TEST); \
		python2.7 -m $(TEST) $(PYFLAGS); \
		)
test32:
	@- $(foreach TEST,$(TESTS), \
		echo === Running python3.2 test: $(TEST); \
		python3.2 -m $(TEST) $(PYFLAGS); \
		)
test33:
	@- $(foreach TEST,$(TESTS), \
		echo === Running python3.3 test: $(TEST); \
		python3.3 -m $(TEST) $(PYFLAGS); \
		)
test34:
	@- $(foreach TEST,$(TESTS), \
		echo === Running python3.4 test: $(TEST); \
		python3.4 -m $(TEST) $(PYFLAGS); \
		)
test35:
	@- $(foreach TEST,$(TESTS), \
		echo === Running python3.5 test: $(TEST); \
		python3.5 -m $(TEST) $(PYFLAGS); \
		)
