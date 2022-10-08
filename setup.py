from gettext import install
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AstroScheduller",
    version="1.0.3.2210",
    author="Wenky",
    author_email="wxia1@fandm.edu",
    description="AstroScheduller algorithms and packages for planning astronomical observations.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AstroScheduller/AstroScheduller",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
        'requests',
        'astropy',
        'Pillow'
    ],
    package_data={
        'astroscheduller': [
            'ashrel/*.png',
            'ashrel/*.ico',
            'ashrel/*.json',
            'ashrel/*.txt',
            'ashrel/*.ash'
        ]
    }
)
