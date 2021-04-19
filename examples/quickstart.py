"""
This example script imports the task_scheduler package and
prints out the version.
"""

import task_scheduler


def main():
    print(
        f"task_scheduler version: {task_scheduler.__version__}"
    )


if __name__ == "__main__":
    main()
