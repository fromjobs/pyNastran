# -*- PyInstaller input file -*-
# -*- mode: python           -*-

try:
    import pyInstaller
    pyInstaller_path = [os.path.dirname(pyinstaller.__file__)]
    print("pyInstaller_path = %r" % pyInstaller_path)
except ImportError:
    pyInstaller_path = []

pyInstaller_path = [r'F:\work\pyNastran\pyNastran\pyinstaller']
IS_H5PY = False
DEBUG = False
IS_RELEASE = True

#-------------------------------------------------------------------------
## this block gets/sets the version so it doesn't use git

#import pyNastran
#pyNastran.is_pynastrangui_exe = True
#pyNastran.__version__ = '%r' % pyNastran.__version__
#pyNastran.__releaseDate__ =  '%r' % pyNastran.__releaseDate__
#pyNastran.__releaseDate2__ = '%r' % datei.strftime('%d %B %Y')

import os
import sys
import shutil
import datetime
from six import PY2

# get pyNastran location
print('sys.version_info.major =', sys.version_info.major)
if sys.version_info.major == 3:
    pkg_path = os.path.abspath(os.path.join('.', '..', 'pyNastran'))
else:
    import pkgutil
    pkg_path = pkgutil.get_loader('pyNastran').filename
init_filename = os.path.join(pkg_path, '__init__.py')
assert os.path.exists(init_filename), init_filename

# getting pyNastran version without using the __init__.py file
# because we need to hack on it
import subprocess
try:
    ghash = subprocess.check_output(['git', 'describe', '--always'], cwd=os.path.dirname(init_filename))
    ghash = ghash.decode('utf-8').rstrip()
except:
    # git isn't installed
    ghash = 'no.checksum.error'

# hacking on the __init___.py file to set:
#   is_pynastrangui_exe = True
init_filename_bkp = init_filename + '.bkp'
shutil.copyfile(init_filename, init_filename_bkp)

print('opening %s to hack the is_pynastrangui_exe flag' % init_filename)
with open(init_filename, 'r') as init_file:
    lines = init_file.readlines()

# update the init.py with:
# - is_pynastrangui_exe = True
#
# and get the version
#
lines2 = []
for line in lines:
    if 'is_pynastrangui_exe = False' in line:
        line = 'is_pynastrangui_exe = True\n'
    elif '__version__ = ' in line:
        # __version__ = '1.1.0+%s' % revision
        version_fmt = line.split("'")[1]  # '1.1.0+%s'
    lines2.append(line)

assert len(lines2) > 8, lines2
with open(init_filename, 'w') as init_file:
    for line in lines2:
        init_file.write(line)

#version = '1.1.0+dev.%s' % ghash
version = version_fmt
if not IS_RELEASE:
    version = version_fmt % ghash

# write the version
version_filename = os.path.join(pkg_path, 'version.py')
with open(version_filename, 'w') as version_file:
    datei = datetime.date.today()
    version_file.write('# -*- coding: utf-8 -*-\n')
    version_file.write('# this file is autogenerated by pyInstaller\n')
    version_file.write('__version__ = %r\n' % version)
    version_file.write('__releaseDate__ = %r\n' % str(datei))  # 2016-2-5
    version_file.write('__releaseDate2__ = %r\n' % datei.strftime('%d %B %Y')) # 5 Feb 2016

#-------------------------------------------------------------------------

#a1 = os.path.join(pkg_path, 'bdf','bdf.py')
#a2 = os.path.join(pkg_path, 'op2','op2.py')
#a3 = os.path.join(pkg_path, 'f06','f06.py')
a4 = os.path.join(pkg_path, 'gui','gui.py')
a5 = os.path.join(pkg_path, 'version.py')

#analyze_files = [a1, a2, a3, a4]
analyze_files = [a4, a5]

icon_path = os.path.join(pkg_path, 'gui', 'icons')

icon_names = os.listdir(icon_path)
icons = []
for icon_name in icon_names:
    i1 = os.path.join('icons', icon_name)   # where to put the icon in the exe
    i2 = os.path.join(icon_path, icon_name) # where the icon is now
    icon = (i1, i2, 'DATA')
    icons.append(icon)

#icon_main = os.path.join(iconPath,'guiDemo_128.ico')
icon_main = 'logo.ico' # pyInstaller doesn't like paths in the ico
                       # it also won't handle png files
assert os.path.exists(icon_main), '%s doesnt exist' % icon_main

#-------------------------------------------------------------------------
# main code

#from PyInstaller import compat
#from os import listdir

##mkldir = compat.base_prefix + "/Lib/site-packages/numpy/core"
#logger = logging.getLogger(__name__)
#logger.info("MKL installed as part of numpy, importing that!")
#binaries = [(mkldir + "/" + mkl, '') for mkl in listdir(mkldir) if mkl.startswith('mkl_')]

#python_path = 'F:\Anaconda'
python_path = os.path.dirname(sys.executable)

if PY2:
    mkl_dlls = [
        os.path.join(python_path, 'Library', 'bin', 'mkl_def.dll'),
        #os.path.join(python_path, 'Library', 'bin', 'mkl_avx2.dll'),  # do I need this?
    ]
else:
    mkl_dlls = [
        os.path.join(python_path, 'evns', 'py35', 'Library', 'bin', 'mkl_def3.dll')
        # others?
    ]

has_mkl_dlls = False
if mkl_dlls:
    mkl_dll_base = os.path.basename(mkl_dlls[0])
    #assert os.path.exists(mkl_dll), '%s doesnt exist' % mkl_dll
    has_mkl_dlls = os.path.exists(mkl_dll_base)

binaries = []
if sys.platform == 'win32':
    binaries = [
        ('msvcp100.dll', 'C:\\Windows\\System32\\msvcp100.dll', 'BINARY'),
        ('msvcr100.dll', 'C:\\Windows\\System32\\msvcr100.dll', 'BINARY'),
    ]
    if has_mkl_dlls:
        for mkl_dll in mkl_dlls:
            binaries.append(
                (mkl_dll_base, mkl_dll, 'BINARY')
            )


print('python_path', python_path)

pathex = pyInstaller_path + [
    python_path,
    os.path.join(python_path, 'Lib'),
    os.path.join(python_path, 'Lib', 'site-packages'),

    pkg_path,
    os.path.join(pkg_path, 'bdf'),
    os.path.join(pkg_path, 'op2'),
    os.path.join(pkg_path, 'f06'),
    os.path.join(pkg_path, 'gui'),
]
excludes = [
    #'unittest',   # why can't I remove this?
    'matplotlib', 'wx', 'nose', 'Tkinter',
    
    'distutils', 'distutils.distutils', 'distutils.errors', 'distutils.os',
    'distutils.re', 'distutils.string', 'distutils.sys',
    'distutils.sysconfig', 'distutils.types', 'distutils.version',

    'beautifulsoup4', 'bitarray', 'bottleneck', 'bzip2', 'cdecimal',
    'cffi', 'comtypes', 'conda-build', 'configobj', 'console_shortcut',
    'cryptography', 'cython', 'dask', 'docutils', 'fastcache', 'flask',
    'freetype', 'funcsigs', 'greenlet', 'grin', 
    
    'idna',
    'ipaddress', 'ipython-notebook', 'ipython-qtconsole',
    'ipython_genutils', 'itsdangerous', 'jedi', 'jinja2', 'jpeg',
    'jsonschema', 'jupyter_client', 'jupyter_core', 'launcher',
    'libsodium', 'markupsafe', 'mistune', 'multipledispatch',
    'nbformat', 'nltk', 'node-webkit', 'nose', 'patsy', 'pickleshare',
    'ply', 'pyasn1', 'pycosat', 'pycparser', 'pycrypto', 'pycurl',
    'pyflakes', 'pyopenssl', 'pyparsing', 'pyreadline', 'pytables',
    'python-dateutil', 'rope', 'scikit-image', 'simplegeneric',
    'singledispatch', 'sockjs-tornado', 'ssl_match_hostname',
    'statsmodels', 'sympy', 'tk', 'toolz', 'ujson', 'unicodecsv',
    'xlrd', 'xlwt', 'zeromq', 'zlib', 'alabaster',
    'anaconda-client', 'appdirs', 'astroid', 'astroid', 'astropy'
    'babel', 'backports_abc', 'blackwidow', 'blaze-core', 'bokeh',
    'boto', 'clyent', 'coverage',
    'curl', 'cycler', 'cytoolz', 'datashape', 'decorator', 'freeimage',
    'gl2ps', 'oce', 'pythonocc-core', 'tbb', 'enum34', 'et_xmlfile',
    'futures', 'gevent', 'gevent-websocket', 'hdf5', 'ipykernel',
    'ipython', 'ipywidgets', 'jdcal', 'jupyter', 'jupyter_console',
    'lazy-object-proxy', 'libtiff', 'llvmlite', 'logilab-common',
    'lxml', 'matplotlib', 'menuinst', 'MeshPy',
    'msvc_runtime', 'nbconvert', 'networkx', 'notebook', 'numba',
    
    'numexpr', 'numexpr.__config__', 'numexpr.__future__', 
    'numexpr._winreg', 'numexpr.cpuinfo', 'numexpr.expressions',
    'numexpr.inspect', 'numexpr.interpreter', 'numexpr.necompiler', 
    'numexpr.numexpr', 'numexpr.numpy', 'numexpr.operator', 'numexpr.os',
    'numexpr.pkg_resources', 'numexpr.platform', 'numexpr.re',
    'numexpr.subprocess', 'numexpr.sys', 'numexpr.tests',
    'numexpr.tests.numexpr', 'numexpr.tests.test_numexpr', 
    'numexpr.threading', 'numexpr.types', 'numexpr.utils', 
    'numexpr.version', 'numexpr.warnings',
    
    'numpydoc', 'odo', 'openmdao', 'openpyxl', 'openssl', 
    
    'pandas', 'pandas._libs', 'pandas._libs.algos', 'pandas._libs.calendar',
    'pandas._libs.collections', 'pandas._libs.csv', 'pandas._libs.datetime',
    'pandas._libs.dateutil', 'pandas._libs.decimal', 'pandas._libs.distutils', 
    'pandas._libs.groupby', 'pandas._libs.hashing', 'pandas._libs.hashtable',
    'pandas._libs.index', 'pandas._libs.interval', 'pandas._libs.join', 
    'pandas._libs.json', 'pandas._libs.lib', 'pandas._libs.locale', 
    'pandas._libs.numbers', 'pandas._libs.numpy', 'pandas._libs.operator', 
    'pandas._libs.os', 'pandas._libs.pandas', 'pandas._libs.parsers',
    'pandas._libs.period', 'pandas._libs.pytz', 'pandas._libs.random',
    'pandas._libs.re', 'pandas._libs.reshape', 'pandas._libs.sparse',
    'pandas._libs.sys', 'pandas._libs.testing', 'pandas._libs.thread',
    'pandas._libs.time', 'pandas._libs.tslib', 'pandas._libs.warnings',
    'pandas._libs.window', 'pandas._version', 'pandas.api', 'pandas.api.types',
    'pandas.api.types.pandas', 'pandas.compat', 'pandas.compat.StringIO',
    'pandas.compat.__builtin__', 'pandas.compat.cPickle', 
    'pandas.compat.cStringIO', 'pandas.compat.chainmap',
    'pandas.compat.chainmap_impl', 'pandas.compat.collections', 
    'pandas.compat.copy', 'pandas.compat.dateutil', 'pandas.compat.distutils',
    'pandas.compat.functools', 'pandas.compat.httplib', 'pandas.compat.inspect',
    'pandas.compat.itertools', 'pandas.compat.numpy', 
    'pandas.compat.numpy.distutils', 'pandas.compat.numpy.function',
    'pandas.compat.numpy.numpy', 'pandas.compat.numpy.pandas', 
    'pandas.compat.numpy.re', 'pandas.compat.openpyxl_compat', 
    'pandas.compat.pandas', 'pandas.compat.pickle', 
    'pandas.compat.pickle_compat', 'pandas.compat.re', 'pandas.compat.struct',
    'pandas.compat.sys', 'pandas.compat.thread', 'pandas.compat.types',
    'pandas.compat.unicodedata', 'pandas.core', 'pandas.core.__future__',
    'pandas.core.algorithms', 'pandas.core.api', 'pandas.core.base', 
    'pandas.core.bottleneck', 'pandas.core.categorical', 'pandas.core.codecs',
    'pandas.core.collections', 'pandas.core.common', 'pandas.core.computation', 
    'pandas.core.computation.abc', 'pandas.core.computation.align',
    'pandas.core.computation.api', 'pandas.core.computation.ast',
    'pandas.core.computation.common', 'pandas.core.computation.datetime',
    'pandas.core.computation.distutils', 'pandas.core.computation.engines',
    'pandas.core.computation.eval', 'pandas.core.computation.expr', 
    'pandas.core.computation.expressions', 'pandas.core.computation.functools',
    'pandas.core.computation.inspect', 'pandas.core.computation.itertools',
    'pandas.core.computation.numexpr', 'pandas.core.computation.numpy',
    'pandas.core.computation.operator', 'pandas.core.computation.ops',
    'pandas.core.computation.pandas', 'pandas.core.computation.pprint', 
    'pandas.core.computation.pytables', 'pandas.core.computation.scope',
    'pandas.core.computation.struct', 'pandas.core.computation.sys', 
    'pandas.core.computation.tokenize', 'pandas.core.computation.warnings',
    'pandas.core.config', 'pandas.core.config_init', 'pandas.core.contextlib',
    'pandas.core.copy', 'pandas.core.datetime', 'pandas.core.distutils', 
    'pandas.core.dtypes', 'pandas.core.dtypes.api', 'pandas.core.dtypes.cast', 
    'pandas.core.dtypes.collections', 'pandas.core.dtypes.common',
    'pandas.core.dtypes.concat', 'pandas.core.dtypes.datetime', 
    'pandas.core.dtypes.dtypes', 'pandas.core.dtypes.generic',
    'pandas.core.dtypes.inference', 'pandas.core.dtypes.missing',
    'pandas.core.dtypes.numbers', 'pandas.core.dtypes.numpy', 
    'pandas.core.dtypes.pandas', 'pandas.core.dtypes.re', 'pandas.core.dtypes.sys',
    'pandas.core.dtypes.warnings', 'pandas.core.frame', 'pandas.core.functools', 
    'pandas.core.gc', 'pandas.core.generic', 'pandas.core.groupby',
    'pandas.core.index', 'pandas.core.indexes', 'pandas.core.indexes.__future__',
    'pandas.core.indexes.accessors', 'pandas.core.indexes.api',
    'pandas.core.indexes.base', 'pandas.core.indexes.category',
    'pandas.core.indexes.datetime', 'pandas.core.indexes.datetimelike',
    'pandas.core.indexes.datetimes', 'pandas.core.indexes.frozen', 
    'pandas.core.indexes.functools', 'pandas.core.indexes.interval',
    'pandas.core.indexes.multi', 'pandas.core.indexes.numeric',
    'pandas.core.indexes.numpy', 'pandas.core.indexes.operator',
    'pandas.core.indexes.pandas', 'pandas.core.indexes.period', 
    'pandas.core.indexes.range', 'pandas.core.indexes.sys', 
    'pandas.core.indexes.timedeltas', 'pandas.core.indexes.warnings',
    'pandas.core.indexing', 'pandas.core.internals', 'pandas.core.itertools',
    'pandas.core.json', 'pandas.core.keyword', 'pandas.core.missing', 
    'pandas.core.nanops', 'pandas.core.numpy', 'pandas.core.operator', 
    'pandas.core.ops', 'pandas.core.pandas', 'pandas.core.panel', 
    'pandas.core.panel4d', 'pandas.core.panelnd', 'pandas.core.re',
    'pandas.core.resample', 'pandas.core.reshape', 'pandas.core.reshape.api',
    'pandas.core.reshape.concat', 'pandas.core.reshape.copy', 
    'pandas.core.reshape.itertools', 'pandas.core.reshape.merge', 
    'pandas.core.reshape.numpy', 'pandas.core.reshape.pandas', 
    'pandas.core.reshape.pivot', 'pandas.core.reshape.re', 'pandas.core.reshape.reshape',
    'pandas.core.reshape.string', 'pandas.core.reshape.tile', 'pandas.core.reshape.util',
    'pandas.core.reshape.warnings', 'pandas.core.series', 'pandas.core.sorting', 
    'pandas.core.sparse', 'pandas.core.sparse.__future__', 'pandas.core.sparse.api',
    'pandas.core.sparse.array', 'pandas.core.sparse.frame', 'pandas.core.sparse.list', 
    'pandas.core.sparse.numpy', 'pandas.core.sparse.pandas', 
    'pandas.core.sparse.scipy_sparse', 'pandas.core.sparse.series', 
    'pandas.core.sparse.warnings', 'pandas.core.strings', 'pandas.core.sys',
    'pandas.core.textwrap', 'pandas.core.tokenize', 'pandas.core.tools', 
    'pandas.core.tools.collections', 'pandas.core.tools.datetime',
    'pandas.core.tools.datetimes', 'pandas.core.tools.dateutil',
    'pandas.core.tools.numeric', 'pandas.core.tools.numpy', 'pandas.core.tools.pandas',
    'pandas.core.tools.timedeltas', 'pandas.core.types', 'pandas.core.util',
    'pandas.core.util.hashing', 'pandas.core.util.itertools', 'pandas.core.util.numpy',
    'pandas.core.util.pandas', 'pandas.core.warnings', 'pandas.core.weakref',
    'pandas.core.window', 'pandas.core.xlsxwriter', 'pandas.datetime', 'pandas.errors',
    'pandas.errors.pandas', 'pandas.io', 'pandas.io.__future__', 'pandas.io.abc',
    'pandas.io.api', 'pandas.io.clipboards', 'pandas.io.codecs', 
    'pandas.io.collections', 'pandas.io.common', 'pandas.io.contextlib',
    'pandas.io.copy', 'pandas.io.csv', 'pandas.io.date_converters', 
    'pandas.io.datetime', 'pandas.io.dateutil', 'pandas.io.distutils', 
    'pandas.io.excel', 'pandas.io.feather_format', 'pandas.io.formats', 
    'pandas.io.formats.__future__', 'pandas.io.formats.common',
    'pandas.io.formats.console', 'pandas.io.formats.csv', 'pandas.io.formats.distutils',
    'pandas.io.formats.format', 'pandas.io.formats.itertools',
    'pandas.io.formats.locale', 'pandas.io.formats.numpy', 'pandas.io.formats.os', 
    'pandas.io.formats.pandas', 'pandas.io.formats.printing', 'pandas.io.formats.shutil',
    'pandas.io.formats.sys', 'pandas.io.formats.terminal', 'pandas.io.formats.textwrap',
    'pandas.io.functools', 'pandas.io.gbq', 'pandas.io.html', 'pandas.io.httplib',
    'pandas.io.itertools', 'pandas.io.json', 'pandas.io.json.collections', 
    'pandas.io.json.copy', 'pandas.io.json.json', 'pandas.io.json.normalize',
    'pandas.io.json.numpy', 'pandas.io.json.os', 'pandas.io.json.pandas', 
    'pandas.io.json.table_schema', 'pandas.io.mmap', 'pandas.io.msgpack', 
    'pandas.io.msgpack._packer', 'pandas.io.msgpack._unpacker',
    'pandas.io.msgpack._version', 'pandas.io.msgpack.collections',
    'pandas.io.msgpack.exceptions', 'pandas.io.msgpack.os', 
    'pandas.io.msgpack.pandas', 'pandas.io.numbers', 'pandas.io.numpy', 'pandas.io.os',
    'pandas.io.packers', 'pandas.io.pandas', 'pandas.io.parsers', 'pandas.io.pickle', 
    'pandas.io.py', 'pandas.io.pytables', 'pandas.io.re', 'pandas.io.sas', 
    'pandas.io.sas.pandas', 'pandas.io.sas.sasreader', 'pandas.io.sql', 'pandas.io.stata',
    'pandas.io.struct', 'pandas.io.sys', 'pandas.io.textwrap', 'pandas.io.time',
    'pandas.io.urllib', 'pandas.io.urllib2', 'pandas.io.urlparse', 'pandas.io.warnings',
    'pandas.io.zlib', 'pandas.json', 'pandas.pandas', 'pandas.plotting',
    'pandas.plotting.__future__', 'pandas.plotting._compat', 'pandas.plotting._converter', 
    'pandas.plotting._core', 'pandas.plotting._misc', 'pandas.plotting._style',
    'pandas.plotting._tools', 'pandas.plotting.collections', 'pandas.plotting.contextlib',
    'pandas.plotting.cycler', 'pandas.plotting.datetime', 'pandas.plotting.dateutil',
    'pandas.plotting.distutils', 'pandas.plotting.math', 'pandas.plotting.matplotlib',
    'pandas.plotting.numpy', 'pandas.plotting.pandas', 'pandas.plotting.re',
    'pandas.plotting.warnings', 'pandas.stats', 'pandas.stats.__future__', 
    'pandas.stats.api', 'pandas.stats.moments', 'pandas.stats.numpy', 'pandas.stats.pandas',
    'pandas.stats.warnings', 'pandas.sys', 'pandas.testing', 'pandas.tools', 
    'pandas.tools.pandas', 'pandas.tools.plotting', 'pandas.tools.sys', 
    'pandas.tools.warnings', 'pandas.tseries', 'pandas.tseries.api', 
    'pandas.tseries.datetime', 'pandas.tseries.dateutil', 'pandas.tseries.frequencies', 
    'pandas.tseries.functools', 'pandas.tseries.numpy', 'pandas.tseries.offsets', 
    'pandas.tseries.operator', 'pandas.tseries.pandas', 'pandas.tseries.pytz', 
    'pandas.tseries.re', 'pandas.tseries.warnings', 'pandas.util',
    'pandas.util.__future__', 'pandas.util._decorators', 'pandas.util._depr_module', 
    'pandas.util._move', 'pandas.util._print_versions', 'pandas.util._tester', 
    'pandas.util._validators', 'pandas.util.codecs', 'pandas.util.contextlib', 
    'pandas.util.datetime', 'pandas.util.distutils', 'pandas.util.functools',
    'pandas.util.importlib', 'pandas.util.inspect', 'pandas.util.locale', 'pandas.util.numpy',
    'pandas.util.os', 'pandas.util.pandas', 'pandas.util.platform', 'pandas.util.pytest',
    'pandas.util.re', 'pandas.util.string', 'pandas.util.struct', 'pandas.util.subprocess', 
    'pandas.util.sys', 'pandas.util.tempfile', 'pandas.util.testing', 'pandas.util.textwrap',
    'pandas.util.traceback', 'pandas.util.types', 'pandas.util.warnings', 'pandas.warnings',
    
    '_pytest', '_pytest.__future__', '_pytest._code', '_pytest._code.__future__',
    '_pytest._code._ast', '_pytest._code._py2traceback', '_pytest._code.bisect',
    '_pytest._code.code', '_pytest._code.inspect', '_pytest._code.py', '_pytest._code.re',
    '_pytest._code.source', '_pytest._code.sys', '_pytest._code.tokenize',
    '_pytest._code.types', '_pytest._code.weakref', '_pytest._pluggy', '_pytest._pytest', 
    '_pytest.argparse', '_pytest.assertion', '_pytest.assertion._ast', 
    '_pytest.assertion._pytest', '_pytest.assertion.ast', '_pytest.assertion.collections', 
    '_pytest.assertion.errno', '_pytest.assertion.fnmatch', '_pytest.assertion.imp', 
    '_pytest.assertion.itertools', '_pytest.assertion.marshal', '_pytest.assertion.os', 
    '_pytest.assertion.pprint', '_pytest.assertion.py', '_pytest.assertion.re',
    '_pytest.assertion.rewrite', '_pytest.assertion.struct', '_pytest.assertion.sys',
    '_pytest.assertion.types', '_pytest.assertion.util', '_pytest.bdb',
    '_pytest.cacheprovider', '_pytest.capture', '_pytest.codecs', '_pytest.collections',
    '_pytest.compat', '_pytest.config', '_pytest.contextlib', '_pytest.debugging',
    '_pytest.doctest', '_pytest.enum', '_pytest.fixtures', '_pytest.fnmatch', 
    '_pytest.freeze_support', '_pytest.functools', '_pytest.helpconfig', '_pytest.hookspec',
    '_pytest.inspect', '_pytest.itertools', '_pytest.json', '_pytest.junitxml',
    '_pytest.main', '_pytest.mark', '_pytest.math', '_pytest.monkeypatch', '_pytest.nose', 
    '_pytest.os', '_pytest.pastebin', '_pytest.platform', '_pytest.py', '_pytest.pytest', 
    '_pytest.python', '_pytest.re', '_pytest.recwarn', '_pytest.resultlog', '_pytest.runner',
    '_pytest.setuponly', '_pytest.setupplan', '_pytest.shlex', '_pytest.skipping',
    '_pytest.sys', '_pytest.tempfile', '_pytest.terminal', '_pytest.time', '_pytest.tmpdir',
    '_pytest.traceback', '_pytest.types', '_pytest.unittest', '_pytest.vendored_packages',
    '_pytest.vendored_packages.inspect', '_pytest.vendored_packages.pluggy', 
    '_pytest.vendored_packages.sys', '_pytest.warnings',

    'path.py', 'pep8', 'pi', 'pip',
    'psutil', 'py', 'pylint', 'pyside','pyside2', 'pytest',
    'pytools', 'pytz', 'pyyaml', 'pyzmq',
    'qtconsole', 'requests', 'ruamel_yaml', 'RunSnakeRun',
    'scikit-learn', 'setuptools',
    'snowballstemmer', 'sphinx', 'sphinx_rtd_theme', 'spyder',
    'spyder-app', 'sqlalchemy', 'sqlitedict', 'SquareMap', 'tornado',
    'traitlets', 'werkzeug', 'wheel',
    'wrapt', 'wxpython', 
    
    'xlsxwriter', 'xlsxwriter.StringIO', 'xlsxwriter.app', 'xlsxwriter.chart',
    'xlsxwriter.chart_area', 'xlsxwriter.chart_bar', 'xlsxwriter.chart_column',
    'xlsxwriter.chart_doughnut', 'xlsxwriter.chart_line', 'xlsxwriter.chart_pie',
    'xlsxwriter.chart_radar', 'xlsxwriter.chart_scatter', 'xlsxwriter.chart_stock',
    'xlsxwriter.chartsheet', 'xlsxwriter.codecs', 'xlsxwriter.collections', 
    'xlsxwriter.comments', 'xlsxwriter.compatibility', 'xlsxwriter.contenttypes', 
    'xlsxwriter.copy', 'xlsxwriter.core', 'xlsxwriter.custom', 'xlsxwriter.datetime', 
    'xlsxwriter.decimal', 'xlsxwriter.drawing', 'xlsxwriter.format', 
    'xlsxwriter.fractions', 'xlsxwriter.io', 'xlsxwriter.operator', 'xlsxwriter.os',
    'xlsxwriter.packager', 'xlsxwriter.re', 'xlsxwriter.relationships', 
    'xlsxwriter.shape', 'xlsxwriter.sharedstrings', 'xlsxwriter.shutil', 
    'xlsxwriter.stat', 'xlsxwriter.struct', 'xlsxwriter.styles', 'xlsxwriter.sys',
    'xlsxwriter.table', 'xlsxwriter.tempfile', 'xlsxwriter.theme', 
    'xlsxwriter.utility', 'xlsxwriter.vml', 'xlsxwriter.warnings',
    'xlsxwriter.workbook', 'xlsxwriter.worksheet', 'xlsxwriter.xmlwriter',
    'xlsxwriter.zipfile',
    
    'xlwings',
    


    # not required...strange...
    'conda', 'conda-env', 'pywin32', 'python', 'vs2008_runtime',
    'pyqt', 'anaconda',

    # things we're using
    'libpng',
    #'sip', 'colorama', 'numpy', 'pillow', 'qt',
    #'vtk', 'six', 'mkl', 'mkl-service',
]
excludes = []

if not IS_H5PY:
    excludes += [
        'h5py', 'h5py._conv', 'h5py._errors', 'h5py._hl', 'h5py._hl.attrs',
        'h5py._hl.base', 'h5py._hl.compat', 'h5py._hl.dataset', 'h5py._hl.datatype',
        'h5py._hl.files', 'h5py._hl.filters', 'h5py._hl.group', 'h5py._hl.os',
        'h5py._hl.selections', 'h5py._hl.selections2', 'h5py._hl.six',
        'h5py._hl.sys', 'h5py._objects', 'h5py._proxy', 'h5py.defs',
        'h5py.functools', 'h5py.gc', 'h5py.h5', 'h5py.h5a', 'h5py.h5ac', 'h5py.h5d',
        'h5py.h5ds', 'h5py.h5f', 'h5py.h5fd', 'h5py.h5g', 'h5py.h5i', 'h5py.h5l',
        'h5py.h5o', 'h5py.h5p', 'h5py.h5py', 'h5py.h5r', 'h5py.h5s', 'h5py.h5t',
        'h5py.h5z', 'h5py.highlevel', 'h5py.numpy', 'h5py.operator', 'h5py.platform',
        'h5py.sys', 'h5py.tests', 'h5py.tests.__future__', 'h5py.tests.common',
        'h5py.tests.hl', 'h5py.tests.hl.test_attribute_create',
        'h5py.tests.hl.test_dataset_getitem', 'h5py.tests.hl.test_dataset_swmr',
        'h5py.tests.hl.test_datatype', 'h5py.tests.hl.test_dims_dimensionproxy',
        'h5py.tests.hl.test_file', 'h5py.tests.hl.test_threads', 'h5py.tests.old', 
        'h5py.tests.old.test_attrs', 'h5py.tests.old.test_attrs_data',
        'h5py.tests.old.test_base', 'h5py.tests.old.test_dataset',
        'h5py.tests.old.test_datatype', 'h5py.tests.old.test_dimension_scales',
        'h5py.tests.old.test_file', 'h5py.tests.old.test_file_image', 
        'h5py.tests.old.test_group', 'h5py.tests.old.test_h5', 
        'h5py.tests.old.test_h5f', 'h5py.tests.old.test_h5p', 
        'h5py.tests.old.test_h5t', 'h5py.tests.old.test_objects',
        'h5py.tests.old.test_selections', 'h5py.tests.old.test_slicing',
        'h5py.tests.sys', 'h5py.utils', 'h5py.version', 'h5py.warnings', 
        'h5py.weakref',
    ]

a = Analysis(analyze_files,
             pathex=pathex,
             excludes=excludes,
             hiddenimports=[
                'vtk.vtkCommonPythonSIP', 'vtk.vtkFilteringPythonSIP',
                'PyQt4.QtOpenGL', 'vtk.vtkRenderingPythonSIP',
                'scipy._lib.messagestream', # 'scipy',
                ],
             hookspath=None)
pyz = PYZ(a.pure)

#print("help(EXE) = \n", help(EXE))
exe = EXE(pyz,
          a.scripts,
          a.binaries + binaries + icons,
          a.zipfiles,
          a.datas,
          #exclude_binaries=True,
          name=os.path.join('build\\pyi.win32\\pyNastranGUI', 'pyNastranGUI.exe'),
          debug=DEBUG,
          strip=None,
          #upx=True,
          icon=icon_main,
          console=True )

#print('*'*80)
#print("help(COLLECT) = \n",help(COLLECT))
#coll = COLLECT(exe,
#               a.binaries + binaries + icons,
#               a.zipfiles,
#               a.datas,
#               exclude_binaries=1,
#               #icon=icon_main,
#               strip=None,
#               upx=True,
#               name=os.path.join('dist', 'pyNastranGUI'))

#-------------------------------------------------------------------------
# fix the __init__.py file

shutil.copyfile(init_filename_bkp, init_filename)
os.remove(init_filename_bkp)
