import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flask-ngrok",
    version="0.0.10",
    author="Grant Stafford",
    description="A simple way to demo Flask apps from your machine.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gstaff/flask-ngrok",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    keywords='flask ngrok demo',
    install_requires=['requests'],
    py_modules=['flask_ngrok']
)
