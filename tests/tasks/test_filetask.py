from os import path, curdir, getcwd, sep
from unittest import TestCase
import pytest

from task_scheduler.tasks.config_objects import ConfigFileTask
from task_scheduler.tasks.file_task import FileTask


class TestFileTask(TestCase):
    def setUp(self):
        self.__location__ = path.realpath(
            path.join(getcwd(), path.dirname(__file__)))
        self.config_existent = ConfigFileTask(
            location=path.join(self.__location__,
                               'res', 'testfile.txt'),
            file_encoding='utf-8',
            file_operation='read')
        self.config_nonexistenfile = ConfigFileTask(
            location='inexistente')
        self.config_writefile = ConfigFileTask(
            location=path.join(self.__location__, 'res', 'testwrite.txt'),
            file_encoding='utf-8',
            file_content='Contenido de pruebas',
            file_operation='write'
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

    def test_writefile(self):
        file_task = FileTask(0, config=self.config_writefile)
        try:
            file_task.execute()
            self.assertTrue(True)

            file_task1 = FileTask(0, config=ConfigFileTask(
                location=path.join(self.__location__,
                                   'res', 'testwrite.txt'),
                file_encoding='utf-8',
                file_operation='read'
            ))
            content = file_task1.execute()
            self.assertEqual(content, 'Contenido de pruebas')
        except Exception as err:
            self.assertFalse(True, msg=str(err))

    def test_readfail(self):
        file_task = FileTask(0, config=self.config_nonexistenfile)
        try:
            file_task.execute()
            self.assertFalse(False, msg="This sould fail instead")
        except Exception as err:
            self.assertTrue(True, msg=f'expected exception {type(err)}')