from setuptools import setup, find_packages

setup(
    name='sswave',
    version='0.0.1',
    description='Wavetable processing tools for the Intellijel/Cylonix Shapeshifter Eurorack module',
    long_description=open('README.md').read(),
    author='Eirik Krogstad',
    author_email='eirikkr@gmail.com',
    url='https://github.com/tangram/sswave',
    download_url='https://github.com/tangram/sswave.git',
    license='MIT License',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'clize',
        'matplotlib',
        'numpy',
        'soundfile',
    ],
    entry_points = {
        'console_scripts': ['sswave=sswave:main'],
    },
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Multimedia :: Sound/Audio',
        'Topic :: Utilities'
    ]
)
