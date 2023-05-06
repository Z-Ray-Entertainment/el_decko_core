#!/usr/bin/bash
rm -r ./dist/
python3 -m build
twine check dist/*
#python3 -m twine upload --repository pypi dist/*
#python3 -m twine upload --repository testpypi dist/*