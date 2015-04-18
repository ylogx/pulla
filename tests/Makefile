TESTS = $(wildcard test_*.py)

all.PHONY: test test26 test27 test34 test35

#.PHONY: test

test:
	@- $(foreach TEST,$(TESTS), \
		echo === Running test: $(TEST); \
		python $(TEST); \
		)

test26:
	@- $(foreach TEST,$(TESTS), \
		echo === Running python2.6 test: $(TEST); \
		python2.6 $(TEST); \
		)
test27:
	@- $(foreach TEST,$(TESTS), \
		echo === Running python2.7 test: $(TEST); \
		python2.7 $(TEST); \
		)
test32:
	@- $(foreach TEST,$(TESTS), \
		echo === Running python3.2 test: $(TEST); \
		python3.2 $(TEST); \
		)
test33:
	@- $(foreach TEST,$(TESTS), \
		echo === Running python3.3 test: $(TEST); \
		python3.3 $(TEST); \
		)
test34:
	@- $(foreach TEST,$(TESTS), \
		echo === Running python3.4 test: $(TEST); \
		python3.4 $(TEST); \
		)
test35:
	@- $(foreach TEST,$(TESTS), \
		echo === Running python3.5 test: $(TEST); \
		python3.5 $(TEST); \
		)
