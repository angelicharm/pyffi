#!/usr/bin/python

"""A script for running hacking, surgery, and validation tests.

For validate and surgery tests, exceptions during read will be raised.
For hacking tests, exceptions during read will be passed; these are intended
to hack.
Unlike validate tests, surgery tests modify the original kfm file.

This function in the tester script are called:
   testFile(version, f, kfm)
                    - will be called on every kfm
Not all of these three functions need to be present."""

# --------------------------------------------------------------------------
# ***** BEGIN LICENSE BLOCK *****
#
# Copyright (c) 2007-2008, NIF File Format Library and Tools.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#    * Redistributions in binary form must reproduce the above
#      copyright notice, this list of conditions and the following
#      disclaimer in the documentation and/or other materials provided
#      with the distribution.
#
#    * Neither the name of the NIF File Format Library and Tools
#      project nor the names of its contributors may be used to endorse
#      or promote products derived from this software without specific
#      prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# ***** END LICENSE BLOCK *****
# --------------------------------------------------------------------------

import sys, os
from optparse import OptionParser

import KfmTester

def examples_callback(option, opt, value, parser):
    print """* check if the library can read all files in current directory:

    python kfmtoaster.py read ."""

    sys.exit(0)

def tests_callback(option, opt, value, parser):
    for category in ('hacking', 'surgery', 'validate'):
        print category + ':'
        tests = __import__('KfmTester.' + category)
        tests = getattr(tests, category)
        for test in dir(tests):
            if test[:2] == '__': continue
            print '  ' + test
    sys.exit(0)

def main():
    # parse options and positional arguments
    usage = "%prog [options] <tester> <file>|<folder>"
    description="""Look for a python script "KfmTester.hacking.<tester>",
"KfmTester.validate.<tester>", or "KfmTester.surgery.<tester>"
and use the functions testRoot, testBlock, and testFile therein
for hacking, modifying, or validating <file>, or the files in <folder>."""

    parser = OptionParser(usage, version="%prog $Rev$", description=description)
    parser.add_option("-a", "--arg", dest="arg",
                      type="string",
                      metavar="ARG",
                      help="pass argument ARG to tester")
    parser.add_option("--examples",
                      action="callback", callback=examples_callback,
                      help="show examples of usage and exit")
    parser.add_option("-v", "--verbose", dest="verbose",
                      type="int",
                      metavar="VERBOSE",
                      default=1,
                      help="verbosity level: 0, 1, or 2 [default: %default]")
    parser.add_option("--testers",
                      action="callback", callback=tests_callback,
                      help="list all testers and exit")
    # TODO
##    parser.add_option("-f", "--filename", dest="filename",
##                      metavar="FILE",
##                      help="write output to FILE instead of to the terminal")
    (options, args) = parser.parse_args()

    if len(args) != 2:
        parser.error("incorrect number of arguments (two required)")

    # get tester and top folder/file
    test_str = args[0]
    top = args[1]

    try:
        testers = __import__('KfmTester.hacking.' + test_str)
        test = getattr(testers.hacking, test_str)
        raisereaderror = False
        mode = 'rb'
    except ImportError:
        try:
            testers = __import__('KfmTester.validate.' + test_str)
            test = getattr(testers.validate, test_str)
            raisereaderror = True
            mode = 'rb'
        except ImportError:
            try:
                testers = __import__('KfmTester.surgery.' + test_str)
                test = getattr(testers.surgery, test_str)
                raisereaderror = True
                mode = 'r+b'
            except ImportError:
                # either tester was not found, or had an error while importing
                parser.error("tester '%s' not found" % test_str)

    testFile = getattr(test, 'testFile',
                       KfmTester.testFileOverwrite if mode == 'r+b' else None)

    # run tester
    KfmTester.testPath(
        top,
        testFile = testFile,
        raisereaderror = raisereaderror, mode = mode, verbose = options.verbose,
        arg = options.arg)

# if script is called...
if __name__ == "__main__":
    main()