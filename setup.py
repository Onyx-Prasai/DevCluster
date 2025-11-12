from setuptools import find_packages, setup
from typing import List

def get_requirements(file_path: str) -> List[str]:
    """
    This function will return the list of requirements for the project
    from the given requirements file.
    Also avoids -e .
    
    param file_path: str : path to the requirements file
    return: List[str] : list of requirements
    """
    with open(file_path, "r") as f:
        return [line.strip() for line in f.readlines() if line.strip() and not line.startswith("-e")]

setup(
    name="DevCluster360",
    version="0.1.0",
    author="Khagendra Neupane",
    packages=find_packages(),
    install_requires=get_requirements(file_path="requirements.txt"),
    description="A comprehensive tool for github contribution analysis and visualization",
    author_email="nkhagendra1@gmail.com"  
)