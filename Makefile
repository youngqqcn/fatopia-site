
.PHONY: build
build:
	pyside6-uic fantopia.ui -o ui_fantopia.py

run: build
	python3 widget.py


