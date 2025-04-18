#!/bin/bash
black . --exclude venv
isort . --skip venv
flake8 . --exclude venv