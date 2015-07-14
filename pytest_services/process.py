"""Subprocess related functions."""
try:
    import subprocess32 as subprocess
except ImportError:
    import subprocess


def check_output(*popenargs, **kwargs):
    """Run command with arguments and return its output (both stdout and stderr) as a byte string.

    If the exit code was non-zero it raises a CalledProcessWithOutputError.
    """
    if 'stdout' in kwargs:
        raise ValueError('stdout argument not allowed, it will be overridden.')

    if 'stderr' in kwargs:
        raise ValueError('stderr argument not allowed, it will be overridden.')

    process = subprocess.Popen(
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        *popenargs, **kwargs)
    output, err = process.communicate()
    retcode = process.poll()
    if retcode:
        cmd = kwargs.get("args")
        if cmd is None:
            cmd = popenargs[0]
        raise CalledProcessWithOutputError(retcode, cmd, output, err)

    return output, err


class CalledProcessWithOutputError(subprocess.CalledProcessError):

    """An exception with the steout and stderr of a failed subprocess32."""

    def __init__(self, returncode, cmd, output, err):
        """Assign output and error."""
        super(CalledProcessWithOutputError, self).__init__(returncode, cmd)

        self.output = output
        self.err = err

    def __str__(self):
        """str representation."""
        return super(CalledProcessWithOutputError, self).__str__() + ' with output: {0} and error: {1}'.format(
            self.output, self.err)
