from setuptools import setup, find_packages
from sweettea.version import version

setup(name='sweettea',
      version=version,
      description='SweetTea CLI',
      url='https://github.com/sweettea-io/cli',
      author='Ben Whittle',
      author_email='ben@sweettea.io',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
        'click',
        'awesome-slugify',
        'requests',
        'requests-toolbelt',
        'tinynetrc',
        'pyyaml',
        'gitpython',
        'clint'
      ],
      entry_points='''
        [console_scripts]
        st=sweettea.main:cli
      ''')