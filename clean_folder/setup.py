from setuptools import setup
args_dict = {
    "name": "clean_folder",
    "version": "0.0.1",
    "description": "Sort files code",
    "url": "http://github.com/LenaBoychuk/clean_folder",
    "author": "Lena",
    "author_email": "Boychuklena27@gmail.com",
    "license": "MIT",
    "packages": ["clean_folder"],
    "install_requires": [],
    "entry_points": {'console_scripts': ['clean-folder = clean_folder.clean:main']}
    }
def do_setup(args_dict):
    setup(**args_dict)

if __name__ == '__main__':
    do_setup(args_dict)
