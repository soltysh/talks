import tempfile
import shutil
import os.path
from contextlib import contextmanager

@contextmanager
def tempdir():
    """Using generator function as a context manger"""
    dirname = tempfile.mkdtemp()
    try:
        yield dirname # here the magic happens
    finally:
        shutil.rmtree(dirname)

if __name__ == '__main__':
    with tempdir() as dirname:
        print(dirname, os.path.isdir(dirname))
