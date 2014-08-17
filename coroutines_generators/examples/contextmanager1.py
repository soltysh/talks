import tempfile
import shutil
import os.path

class tempdir(object):
    """Simple context manager creating temporary directory"""

    def __enter__(self):
        """ Enter method, responsible for creating the temporary directory and
        returning the directory name to the user"""
        self.dirname = tempfile.mkdtemp()
        return self.dirname

    def __exit__(self, exc, val, tb):
        """Exit method, responsible for removing temporary directory"""
        shutil.rmtree(self.dirname)

if __name__ == '__main__':
    with tempdir() as dirname:
        print(dirname, os.path.isdir(dirname))
