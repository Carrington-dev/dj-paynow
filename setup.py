# ============================================================================
# setup.py
# ============================================================================
"""
dj-paynow: Django PayNow Integration Library
"""
from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

def get_version():
    with open('paynow/__init__.py', 'r') as f:
        for line in f:
            if line.startswith('__version__'):
                return line.split('=')[1].strip().strip('"').strip("'")
    return '0.0.1'

setup(
    name='dj-paynow',
    version=get_version(),
    author='Carrington Muleya',
    author_email='carrington.muleya@outlook.com',
    description='Django PayNow integration library for Zimbabwean payments',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/carrington-dev/dj-paynow',
    project_urls={
        'Bug Reports': 'https://github.com/carrington-dev/dj-paynow/issues',
        'Source': 'https://github.com/carrington-dev/dj-paynow',
        'Documentation': 'https://carrington-dev.github.io/dj-paynow/',
    },
    packages=find_packages(exclude=['tests*', 'docs*', 'examples*']),
    include_package_data=True,
    install_requires=[
        'Django>=3.2',
        'djangorestframework>=3.12.0',
        'requests>=2.25.0',
    ],
    extras_require={
        'dev': [
            'pytest>=7.0.0',
            'pytest-django>=4.5.0',
            'pytest-cov>=4.0.0',
            'black>=22.0.0',
            'flake8>=5.0.0',
            'isort>=5.10.0',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.8',
    keywords='django paynow payment gateway zimbabwe ecocash onemoney',
    license='MIT',
)

