from unittest import TestCase
from julius_controller import JuliusController
import os


class TestJuliusController(TestCase):
    def setUp(self):
        julius_path = '%s/julius/kit/dictation-kit-v4.4/bin/osx/julius' % os.getcwd()
        self.julius_controller = JuliusController(shell_path='/bin/bash', julius_path=julius_path)
        config = '%s/julius/kit/dictation-kit-v4.4/main.jconf' % os.getcwd()
        self.julius_controller.add_config(config)
        config = '%s/julius/kit/dictation-kit-v4.4/am-gmm.jconf' % os.getcwd()
        self.julius_controller.add_config(config)
        self.julius_controller.start()

    def tearDown(self):
        self.julius_controller.end()

    def test_file_recognize(self):
        file = '%s/tests/data/test.wav' % os.getcwd()
        obj_list = self.julius_controller.recognize_file(file)
        print(obj_list)
        self.assertRegex(obj_list[0]['sentence'], 'これ は マイク の テスト です 。\n|\r\n|\r')

    def test_file_recognize_continuous(self):
        file = '%s/tests/data/test.wav' % os.getcwd()
        obj_list = self.julius_controller.recognize_file(file)
        self.assertRegex(obj_list[0]['sentence'], 'これ は マイク の テスト です 。\n|\r\n|\r')
        obj_list = self.julius_controller.recognize_file(file)
        self.assertRegex(obj_list[0]['sentence'], 'これ は マイク の テスト です 。\n|\r\n|\r')

    def test_has_all_keys(self):
        file = '%s/tests/data/test.wav' % os.getcwd()
        obj_list = self.julius_controller.recognize_file(file)
        for obj in obj_list:
            for key in obj.keys():
                self.assertIn(key, JuliusController.JULIUS_PARAMS, obj)
