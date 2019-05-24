import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='pytest-tests-execution-flow',
     version='0.0.1',
     author="Sergii Kremko",
     author_email="sergii.kremko@gmail.com",
     description="Plugin for pytest",
     long_description=long_description,
     long_description_content_type='text/markdown',
     py_modules=['pytest_test_execution_flow'],
     entry_points={'pytest11': ['execution_flow = pytest_test_execution_flow']},
     install_requires=[
       'pytest>=4.1.0'
     ]
 )
