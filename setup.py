
#it basically make your project as a package that you can use in another project as well and you can even deploy in py py so that anyone else can install and use

# setup.py is a build and installation script for Python projects.
# It tells Python (and tools like pip) how to install, package, or distribute your project.
# In short:
# It’s the “configuration file” that defines your project’s metadata, dependencies, and how it should be installed or shared.

from setuptools import find_packages, setup
from typing import List

# this '-e .' that is also mentioned in the requirements.txt this autometically triggers the setup.py
HYPHEN_E_DOT='-e .'

def get_requirements(file_path:str)->List[str]:
    '''
    this function will return the list of requirements that we can use in the setup
    '''
    requirements = [] #where the requirements.txt lib will be written
    #code to read requirements.txt and write them in requiremenrs list
    with open(file_path) as file_obj:
        requirements= file_obj.readlines() #this will read each line in the requirements.txt but will add \n so to remove this
        requirements=[req.replace("\n", "") for req in requirements] #list comprehension to remove \n

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)


    return requirements




setup(
    name='project',
    version='0.0.1',
    author='Nikita',
    author_email='nikitasinghak257@gmail.com',
    packages=find_packages(),
    install_requires = get_requirements('requirements.txt')
)