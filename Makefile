install:
	poetry run ampy --port "$(DEVICE)" put pico_hood/__init__.py main.py
