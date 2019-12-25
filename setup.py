import os
from setuptools import setup


def read(relpath: str) -> str:
	with open(os.path.join(os.path.dirname(__file__), relpath)) as f:
		return f.read()


setup(
	name = 'circular-buffer',
	version = read('version.txt').strip(),
	description = 'Efficient circular buffer implementation in Python with optional Numba JIT compilation',
	long_description = read('README.rst'),
	author = 'Jan Škoda',
	author_email = 'skoda@jskoda.cz',
	url = 'https://github.com/leftys/circular-buffer',
	license = 'MIT',
	extras_require = {
		'numba': ['numba>=0.46.0'],
	},
	packages = [
		'circular_buffer',
	],
	classifiers = [
		'Development Status :: 4 - Beta',
		'License :: OSI Approved :: MIT License',
		'Natural Language :: English',
		'Programming Language :: Python :: 3 :: Only',
		'Programming Language :: Python :: 3.6',
	]
)
