#!/bin/bash
mkdir -p dist/library
mkdir -p dist/holder

cp -r src/* dist/
cp -n ../library/* dist/library/
cp ../holder/holder.stl dist/holder/holder.stl
