.PHONY: env

env: env/setup-stamp

env/setup-stamp: setup.py
	python3 -m venv env
	touch $@
	env/bin/python3 env/bin/pip3 install --editable .
