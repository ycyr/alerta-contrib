
from setuptools import setup, find_packages

version = '0.0.3'

setup(
    name="alerta-easyvista",
    version=version,
    description='Alerta plugin for EasyVista Lookup',
    url='https://github.com/ycyr/alerta-contrib',
    license='MIT',
    author='Yanick Cyr',
    author_email='yanick.cyr@gmail.com',
    packages=find_packages(),
    py_modules=['alerta_easyvista'],
    install_requires=[
        'requests'
    ],
    include_package_data=True,
    zip_safe=True,
    entry_points={
        'alerta.plugins': [
            'easyvista = alerta_easyvista:TriggerTicket'
        ]
    }
)
