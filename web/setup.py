# pylint: disable=missing-module-docstring
from setuptools import setup, find_packages

setup(
    name='chatbot-lti-app',
    version='1.0.0',
    url='https://gerrit.instructure.com/plugins/gitiles/chatbot-lti',
    author='Dustin Cowles',
    author_email='dustin@dustincowles.com',
    description='A simple LTI app providing an interactive chatbot.',
    packages=find_packages(),
    install_requires=[]
)
