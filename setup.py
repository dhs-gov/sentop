import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='sentop',  
     version='0.1',
     scripts=['sentop'] ,
     author="Stephen Quirolgico",
     author_email="stephen.quirolgico@gmail.com",
     description="A sentiment analysis and topic modeling package",
     long_description=long_description,
   long_description_content_type="text/markdown",
     url="https://github.com/dhs-gov/sentop",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: Public Domain",
         "Operating System :: OS Independent",
     ],
 )