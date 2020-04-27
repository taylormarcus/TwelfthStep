from setuptools import find_packages, setup


setup(
    name="TwelfthStep",
    version="0.0.1",
    packages=find_packages(),
    package_data={"twelfthstep": ["database/*.db"]},
    url="https://github.com/taylormarcus/TwelfthStep",
    license="MIT",
    author="Marcus T Taylor",
    description="Randomly generates topics for twelve step meetings.",
    install_requires=["click", "tabulate"],
    python_requires=">=3.0",
    entry_points={
        "console_scripts": [
            "ts-editor=twelfthstep.editor:main",
            "ts-selector=twelfthstep.selector:main"
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
)
