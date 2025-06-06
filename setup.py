from setuptools import setup, find_packages

setup(
    name='webscanner',
    version='0.1.0',
    description='Python tool for detecting security vulnerabilities on your own webpage.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    author='Brady Graff',
    license='MIT',
    packages=find_packages(),
    python_requires='>=3.10',
    install_requires=[
        'beautifulsoup4',
        'lxml',
        'requests',
        'rich',
    ],
    entry_points={
        'console_scripts': [
            'webscanner=scanner.main:main',
        ],
    },
)
