from setuptools import find_packages,setup
from typing import List

def get_requirements()->List[str]:
    try:
        with open('requirements.txt','r') as file:
            req_lst:List[str]=[]
            lines=file.readlines()
            for line in lines:
                line=line.strip()
                requirement=line.replace('\n','')
                if requirement!='-e .':
                    req_lst.append(requirement)
                
    except FileNotFoundError:
        print('requirements.txt file not Found!')
    return req_lst


setup(
    name='Network Security',
    author='Krish Kataria',
    version="0.0.1",
    author_email='kkrishkataria@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements()
    
)