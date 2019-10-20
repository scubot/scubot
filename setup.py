import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="scubot-core",
    version="1.0.0.dev",
    author="Scubot Team",
    description="Scubot's basic operating functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/scubot/scubot",
    packages=setuptools.find_packages(),
    install_requires=[
        "discord"

        "noaa @ git+https://github.com/scubot/noaa.git"
        "@rewrite"

        "noaa @ git+https://github.com/scubot/tags.git"
        "@package"
    ],
    entry_points={
        'scubot': 'bot.main'
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
