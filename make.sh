#!/bin/zsh

rm -rf dist
rm -rf src/bambu_printer_manager.egg-info
rm -rf build

python -m build
