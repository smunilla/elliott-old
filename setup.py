from setuptools import setup
import os


NAME = 'elliott'
OWNER = 'smunilla'
VERISON_FILE = os.path.join(os.path.dirname(__file__), 'src', 'VERSION')
VERSION = open(VERISON_FILE).read().strip()

with open('requirements.txt') as f:
    INSTALL_REQUIRES = f.read().splitlines()

setup(
    name='elliott',
    version=VERSION,
    description=('Python CLI Tool for interfacing with Errata Tool'),
    author='Sam Munilla',
    author_email='smunilla@redhat.com',
    url='https://github.com/smunilla/elliott',
    license='MIT',
    # packages=find_packages(),
    scripts=['src/elliott', 'src/elliott.py'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 2.7'
    ],
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
)
