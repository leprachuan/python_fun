#!/usr/bin/env python

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE UNIVERSITY OF CALIFORNIA BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Targeting python2.6 for RHEL6 compatibility

import collections
import optparse
import logging
import subprocess
import sys


# Backported check_output from 2.6
# From: https://gist.github.com/edufelipe/1027906
def check_output(*popenargs, **kwargs):
    r"""Run command with arguments and return its output as a byte string.

    Backported from Python 2.7 as it's implemented as pure python on stdlib.

    >>> check_output(['/usr/bin/python', '--version'])
    Python 2.6.2
    """
    process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
    output, unused_err = process.communicate()
    retcode = process.poll()
    if retcode:
        cmd = kwargs.get("args")
        if cmd is None:
            cmd = popenargs[0]
        error = subprocess.CalledProcessError(retcode, cmd)
        error.output = output
        raise error
    return output




def zpool_list():
    """ Get the list of all zpools.  Capture capacity & health along
    the way. """
    out = check_output(['/sbin/zpool', 'list'])
    lines = out.splitlines()
    del lines[0]
    zpools = []
    # NAME   SIZE  ALLOC   FREE    CAP  DEDUP  HEALTH  ALTROOT
    for line in lines:
        columns = map(lambda s: s.strip(), line.split())
        zpool = {}
        zpool['name'] = columns[0]
        zpool['capacity'] = float(columns[4].strip('%'))
        health_s = columns[6]
        if health_s in ZPOOL_HEALTH:
            zpool['health'] = ZPOOL_HEALTH[health_s]
        else:
            zpool['health'] = 100
        zpools.append(zpool)
    return zpools


def zpool_find_errors(pool_name=tank2):
    """ There is no property that corresponds cleanly to the errors
    output line from `zpool status`.  Instead the full status command
    is run and anything other than 'no errors' is considered bad. """
    out = check_output(['/sbin/zpool', 'status', pool_name])
    has_errors = 1
    for line in out.splitlines():
        if 'errors:' in line:
            msg = line.split('errors:')[1].strip()
            if msg == 'No known data errors':
                has_errors = 0
                break
    return has_errors

def main():
    zpool_find_errors()

if __name__ == '__main__':
    main()
    
