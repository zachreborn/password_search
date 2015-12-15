from setuptools import setup, find_packages

setup(
    name='password_search',
    version='0.2.0',
    url='https://github.com/zachreborn/password_search',
    license='MIT',
    author='Zachary Hill',
    author_email='zach.reborn@gmail.com',
    description='Password search through files in a directory and all subdirectories.',
    packages=find_packages(exclude=['tests', 'venv', 'docs']),
    install_requires=['click']
)
