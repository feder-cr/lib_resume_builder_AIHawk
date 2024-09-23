default: dev

all: dev test

venv:
	test -d .venv || python3 -m venv .venv

activate:
	test -d .venv && . .venv/bin/activate

dev: venv
	. .venv/bin/activate && python3 setup.py develop

lint:
	. .venv/bin/activate && pre-commit run --all-files

unittest: dev
	. .venv/bin/activate && cd lib_resume_builder_AIHawk/unit-test && python3 -m unittest pdf_generation

clean:
	rm -rf .venv
	rm -rf dist
	rm -rf lib_resume_builder_AIHawk.egg-info
	rm -rf log

.PHONY: dev install unittest