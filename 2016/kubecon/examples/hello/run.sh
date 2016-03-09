#!/bin/bash -e

kubectl run hello --image=python:3.5.1 --restart=Never -- python -c 'print("Hello world!")'
