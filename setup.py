from setuptools import setup

setup(name='bot',
      version='1.0',
      description='Weather bot',
      url='https://github.com/Ub1t/projectadv',
      author='Gromov Vladislav',
      author_email='ubetsf@gmail.com',
      license='MIT',
      packages=['bot'],
      install_requires=[
            'apiai',
            'json',
            'requests',
            'pyowm',
            'datetime',
            'googletrans'

],
      include_package_data=True,
      zip_safe=True)