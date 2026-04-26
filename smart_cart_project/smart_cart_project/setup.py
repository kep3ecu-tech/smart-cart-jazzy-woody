from setuptools import setup
import os
from glob import glob

package_name = 'smart_cart_project'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='hyeon',
    maintainer_email='hyeon@todo.todo',
    description='Smart Cart Project',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'imu_node = smart_cart_project.imu_node:main',
            'motor_node = smart_cart_project.motor_node:main',
            'final_cart = smart_cart_project.final_cart:main',
            'lidar_node = smart_cart_project.lidar_node:main',
        ],
    },
)
