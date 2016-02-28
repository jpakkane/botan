project('botan', 'cpp', version : '1.11.28', license : 'BSD',
  default_options : ['cpp_std=c++11',
                     'warnlevel=3',
                     'buildtype=debugoptimized'])

cpp = meson.get_compiler('cpp')

if cpp.get_id() != 'msvc'
  extra_warnings = ['-Wstrict-aliasing',
    '-Wstrict-overflow=5',
    '-Wcast-align',
    '-Wmissing-declarations',
    '-Wpointer-arith',
    '-Wcast-qual',
    '-Wzero-as-null-pointer-constant',
  ]
else
  extra_warnings = []
endif

# X86-64 specific currently.

ext_libs = [find_library('bz2'),
  find_library('rt', required : false),
  find_library('dl', required : false),
]
ext_deps = [dependency('threads')]

archflags = [] #['-mavx2', '-maes', '-mpclmul']

subdir('src')

botanlib = library('botan-1.11',
  libsrc,
  dependencies : [ext_libs, ext_deps],
  cpp_args : extra_warnings + archflags,
)

botancli = executable('botancli',
  clisrc,
  link_with : botanlib,
  dependencies : [ext_libs, ext_deps],
  cpp_args : extra_warnings + archflags,
)

botantest = executable('botantest',
  testsrc,
  link_with : botanlib,
  dependencies : [ext_libs, ext_deps],
  cpp_args : extra_warnings + archflags,
)

rc = run_command('headersetup.py', meson.current_source_dir(), meson.current_build_dir())

if rc.returncode() != 0
  error(rc.stderr())
endif

# Tests fail because Botan assumes build in source tree so it can't find
# its data files.
#test('botan basic', botantest)

botan_dep = declare_dependency(
  link_with : botanlib,
  include_directories : include_directories('.'),
  )
