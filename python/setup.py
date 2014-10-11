
from distutils.core import setup

setup(name='moratab',
	version='0.1',
	description='Persian markdown convertor.',
	author='Alireza Nourian',
	author_email='alireza.nournia@gmail.com',
	url='http://www.sobhe.ir/moratab/',
	py_modules=['moratab'],
	classifiers=[
		'Natural Language :: Persian',
		'Programming Language :: Python :: 2.7',
		'License :: OSI Approved :: MIT License',
	],
	install_requires=['mistune==0.3.0']
)