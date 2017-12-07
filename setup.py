from setuptools import setup, find_packages
setup(
    name='sckit',
    version='0.1',
    packages=find_packages(),
    author='Shawn Chen',
    author_email='kertansul@gmail.com',
    zip_safe=False,
    install_requires=[
        "httplib2>=0.10.3",
        "google-api-python-client"
    ]
)
