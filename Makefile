TEST_FILES = $(wildcard tests/test_*.py)
TESTS = $(subst .py,,$(subst /,.,$(TEST_FILES)))

all.PHONY: test
#test26 test27 test34 test35

#.PHONY: test

test:
	@- $(foreach TEST,$(TESTS), \
		echo === Running test: $(TEST); \
		python -m $(TEST); \
		)

test26:
	@- $(foreach TEST,$(TESTS), \
		echo === Running python2.6 test: $(TEST); \
		python2.6 -m $(TEST); \
		)
test27:
	@- $(foreach TEST,$(TESTS), \
		echo === Running python2.7 test: $(TEST); \
		python2.7 -m $(TEST); \
		)
test32:
	@- $(foreach TEST,$(TESTS), \
		echo === Running python3.2 test: $(TEST); \
		python3.2 -m $(TEST); \
		)
test33:
	@- $(foreach TEST,$(TESTS), \
		echo === Running python3.3 test: $(TEST); \
		python3.3 -m $(TEST); \
		)
test34:
	@- $(foreach TEST,$(TESTS), \
		echo === Running python3.4 test: $(TEST); \
		python3.4 -m $(TEST); \
		)
test35:
	@- $(foreach TEST,$(TESTS), \
		echo === Running python3.5 test: $(TEST); \
		python3.5 -m $(TEST); \
		)
