#!/bin/bash

rm -rf build
rm -rf dist

rm *.spec

pyinstaller.py --buildpath=dist src/seamless_compiler_gui.py src/seamless_compiler.py

cd dist
mv seamless_compiler_gui seamless_compiler
zip seamless_compiler_linux.zip seamless_compiler/*
mv seamless_compiler_linux.zip ..

cd ..
rm -rf build
rm -rf dist
rm *.spec
rm *.log
