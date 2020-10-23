from setuptools import setup, find_packages
import sys

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('CHANGELOG.md') as history_file:
    history = history_file.read()
with open('requirements.txt') as requirements_file:
    requirements = [req for req in requirements_file.readlines()]

with open('dev-requirements.txt') as dev_requirements_file:
    dev_requirements = [req for req in dev_requirements_file.readlines()]

print("Warning: Plugins are being split out over time. Please ensure you check what is being installed as you upgrade and keep split plugins up to date. The way you upgrade may change in future releases.", file=sys.stderr)
setup(
    name='MirahezeBot_Plugins',
    version='9.0.2',
    description='Sopel Plugins for Miraheze Bots',
    long_description=readme + '\n\n' + history,
    long_description_content_type='text/markdown',  # This is important!
    author='MirahezeBot Contributors',
    author_email='bots@miraheze.org',
    url='https://github.com/MirahezeBots/MirahezeBots',
    packages=find_packages('.'),
    include_package_data=True,
    install_requires=requirements,
    tests_require=dev_requirements,
    test_suite='tests',
    license='Eiffel Forum License, version 2',
)
