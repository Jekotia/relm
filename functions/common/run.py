from subprocess import check_output, CalledProcessError
import tempfile

def func_run(*args):
    with tempfile.TemporaryFile() as t:
        try:
            out = check_output(args, stderr=t)
            return  0, out
        except CalledProcessError as e:
            t.seek(0)
            return e.returncode, t.read()
