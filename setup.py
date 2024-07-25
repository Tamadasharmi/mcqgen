from setuptools import find_packages,setup

setup(
    name='mcqgenrator',
    version='0.0.1',
    author='tamada sharmi',
    author_email='tsharmi12341234@gmail.com',
    install_requires=["huggingface_hub","langchain","streamlit","python-dotenv","PyPDF2"],
    packages=find_packages()
)