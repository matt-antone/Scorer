from setuptools import setup, find_packages

setup(
    name="scorer",
    version="1.0.0",
    packages=find_packages(),
    package_data={
        "": [
            "*.kv",
            "assets/*",
            "assets/fonts/*",
            "assets/images/*",
            "assets/sounds/*",
        ]
    },
    install_requires=[
        "kivy>=2.3.0",
        "kivymd>=1.1.1",
        "flask>=2.0.0",
        "flask-socketio>=5.0.0",
        "eventlet>=0.30.0",
    ],
    python_requires=">=3.11",
) 