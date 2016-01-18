try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="gorgon",
    version="0.1",
    description='Gorgon MMO public JSON files parser.',
    long_description=open("README.md").read(),
    license="MIT",
    url="https://dmnthia.github.io",
    author="Dementhia",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],

    install_requires=[
        "mako>=1.0.3",
        "IPython>=2.3.0",
        "ipdb>=0.8.1"
    ],
    packages=["gorgon"],
    scripts=["scripts/generate_website.py", "scripts/download_version.sh", "scripts/find_latest_version.sh"]
)
