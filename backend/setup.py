from setuptools import setup, find_packages

setup(
    name="samfair",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "scikit-learn",
        "faker",
        "playwright",
        "joblib",
        "reportlab"
    ],
    author="Hackathon Team",
    description="SamFair: Algorithmic bias audit and Post-Prediction Neural Linking library",
    long_description=open("README.md", "r").read() if True else "",
    long_description_content_type="text/markdown",
    url="https://github.com/samfair/samfair",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.8",
)
