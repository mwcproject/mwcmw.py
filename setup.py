import setuptools

setuptools.setup(
    name='mwcmw.py',
    version='0.1.1',
    packages=['mwcmw.py'],
    license='MIT',
    description = 'Python wrappers around the MWC wallet V3 and MWC node V2 APIs',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author = 'MWC Developers',
    author_email = 'info@mwc.mw',
    install_requires=['requests', 'eciespy', 'coincurve', 'Crypto'],
    url = 'https://github.com/mwcproject/mwcmw.py.py',
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    )
