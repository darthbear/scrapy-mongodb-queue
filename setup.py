from setuptools import setup

setup(
    name='scrapy-mongodb-queue',
    version='0.1.0',
    description='Scrapy queue that uses MongoDB',
    keywords='scrapy mongo mongodb queue scheduler',
    license='New BSD License',
    author="Francois Dang Ngoc",
    author_email='francois.dangngoc@gmail.com',
    url='http://github.com/darthbear/scrapy-mongodb-queue/',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
    ],
    packages=[
        'scrapy_mongodb_queue',
    ],
    install_requires=[
        'pymongo',
    ],
)
