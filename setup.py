from setuptools import find_packages, setup


with open('README.md', 'r') as f:
    readme = f.read()

with open('CHANGELOG.rst', 'r') as f:
    changes = f.read()

# def parse_requirements(filename):
#     ''' Load requirements from a pip requirements file '''
#     with open(filename, 'r') as fd:
#         lines = []
#         for line in fd:
#             line.strip()
#             if line and not line.startswith("#"):
#                 lines.append(line)
#     return lines


if __name__ == '__main__':
    setup(
        name='task_scheduler',
        description='Task Manager',
        #install_requires='requirements',
        python_requires='>=3.5',
        #version="0.1.0",
        # long_description='\n\n'.join([readme, changes]),
        # license='MIT license',
        url='https://github.com/strymsg/task-scheduler-at',
        # version=version,
        author='Edson and Rodrigo',
        author_email='',
        maintainer='Edson and Rodrigo',
        maintainer_email='',
        keywords=['task_scheduler'],
        # package_dir={'': 'src'},
        packages=find_packages(include=['task_scheduler', 'task_scheduler.*', 'configs', 'tests']),
        zip_safe=False,
        classifiers=['Development Status :: 3 - Alpha',
                     'Intended Audience :: Developers',
                     'Programming Language :: Python :: 3.6',
                     'Programming Language :: Python :: 3.7',
                     'Programming Language :: Python :: 3.8']
    )
