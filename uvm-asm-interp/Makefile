PY = python
ASM = src/main.py

.PHONY: spec-test assemble

spec-test:
	$(PY) $(ASM) programs/spec_tests.csv spec_tests.bin --test

assemble:
	$(PY) $(ASM) programs/spec_tests.csv spec_tests.bin