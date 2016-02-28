#!/usr/bin/env python3

import os, sys, shutil, subprocess, tempfile

src_root = sys.argv[1]
build_root = sys.argv[2]

assert(os.path.isabs(src_root))

includedir = os.path.join(build_root, 'botan')
internaldir = os.path.join(includedir, 'internal')

if os.path.exists(includedir):
    sys.exit(0)

os.makedirs(includedir)
os.makedirs(internaldir)

for root, dirs, files in os.walk(os.path.join(src_root, 'src/lib')):
    for f in files:
        if f.endswith('.h'):
            absf = os.path.join(root, f)
            # Copy because symlinks do not work on all platforms.
            shutil.copy2(absf, includedir)
            # Ugly but will do for now.
            shutil.copy2(absf, internaldir)

# Run Botan's own configure to generate build.h.
# It does not support out of tree builds so this.

with tempfile.TemporaryDirectory() as tdir:
    tname = os.path.join(tdir, 'botan')
    shutil.copytree(src_root, tname)
    tsrc = os.path.join(tname, os.path.split(src_root)[-1])
    shutil.rmtree(os.path.join(tname, 'build'), ignore_errors=True)
    subprocess.check_call(['./configure.py',
                           '--disable-sse2',
                           '--disable-ssse3',
                           '--disable-avx2',
                           '--disable-aes-ni',
                           '--disable-altivec',
                           ], cwd=tname)
    buildh = os.path.join(tname, 'build/include/botan/build.h')
    shutil.copy2(buildh, includedir)

