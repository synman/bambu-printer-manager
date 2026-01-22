#!/bin/zsh

rm -rf dist
rm -rf src/bambu_printer_manager.egg-info
rm -rf build

pip uninstall -y bambu-printer-manager
python -m build
# pip install .
