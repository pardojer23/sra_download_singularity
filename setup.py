from setuptools import setup, find_packages

setup(name='sra_download',
      version='0.01',
      description='download sra data using slurm and singularity',
      author='Jeremy Pardo',
      author_email='mezeg39@gmail.com',
      packages=find_packages(),
      install_requires=[
                'gspread',
                'oauth2client',
                'pandas'])
