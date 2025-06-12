from setuptools import setup, find_packages

setup(
    name="scorer",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "kivy>=2.3.0",
        "flask>=3.0.0",
        "flask-socketio>=5.3.0",
        "eventlet>=0.33.0",
        "pytest>=8.0.0",
    ],
    python_requires=">=3.11",
) 