from os import path, curdir, getcwd, sep
from unittest import TestCase
import pytest

from task_scheduler.tasks.config_objects import ConfigFileTask
from task_scheduler.tasks.file_task import FileTask


class TestFileTask(TestCase):
    def setUp(self):
        __location__ = path.realpath(
            path.join(getcwd(), path.dirname(__file__)))
        self.config_existent = ConfigFileTask(
            location=path.join(__location__,
                               'res', 'testfile.txt'),
            file_encoding='utf-8',
            type='read')
        self.config_nonexistenfile = ConfigFileTask(location='nonexists')
        self.config_writefile = ConfigFileTask(
            location=path.join(curdir, 'res', 'testfile.txt'),
            file_encoding='utf-8',
            type='write'
        )
    def tearDown(self):
        self.config_existent = None
        self.config_nonexistenfile = None
        self.config_writefile = None

    def test_readfile(self):
        file_task = FileTask(0, config=self.config_existent)
        content = file_task.execute()
        #print(content)
        self.assertTrue(content.startswith('TEST STRATEGY'))
        self.assertTrue(content.endswith('strategy'))
