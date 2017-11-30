from setuptools import setup, find_packages

setup(name='tensorci',
      version='0.0.1',
      description='TensorCI CLI',
      author='Ben Whittle',
      author_email='benwhittle31@gmail.com',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      install_requires=['Click'],
      entry_points='''
        [console_scripts]
        tensorci=tensorci.main:cli
      ''')