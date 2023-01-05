#!/usr/bin/bash
rm -r ./dist/
python3 -m build
twine check dist/*


