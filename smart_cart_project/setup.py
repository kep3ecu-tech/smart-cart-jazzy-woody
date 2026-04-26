from setuptools import setup
import os
from glob import glob

package_name = 'smart_cart_project'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],
    data_files=[
        (os.path.join('share', package_name, 'launch'), glob(os.path.join('launch', '*launch.[pxy][yma]*'))),
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'maps'), glob('maps/*')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='hyeon',
    maintainer_email='hyeon@todo.todo',
    description='Smart Cart Project with TB6612FNG and Sensors',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'imu_node = smart_cart_project.imu_node:main',
            'motor_node = smart_cart_project.motor_node:main',
            'lidar_node = smart_cart_project.lidar_node:main',
            'ultrasonic_node = smart_cart_project.ultrasonic_node:main',
            'final_cart = smart_cart_project.final_cart:main',
            'simple_nav = smart_cart_project.path_planner:main',
            'fake_odom = smart_cart_project.fake_odom:main',
        ],
    },
)
