from setuptools import setup

setup(
    name='pyhulu',
    version='0.1.0',
    description='Python library for interacting with the E2E encrypted Hulu API',
    url='https://github.com/truedread/pyhulu',
    author='truedread',
    author_email='truedread11@gmail.com',
    license='GNU GPLv3',
    packages=['pyhulu'],
    install_requires=['pycryptodomex', 'requests'],
    classifiers=[
        'Environment :: Console',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Utilities'
    ]
)
