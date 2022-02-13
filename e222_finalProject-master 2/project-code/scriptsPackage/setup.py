from setuptools import setup

setup(name='scriptsPackage', 
      version='0.0',
      description='Package of all of the scripts to run the service',
      url='https://github.com/eth-nn/beatsaver-Predictor',
      author='Eth N',
      author_email='30096019+eth-nn@users.noreply.github.com',
      license='MIT',
      packages=['scrape','mongoInterface','model','data', 'csvHandler','pandasCleaning'],
      zip_safe=False)
