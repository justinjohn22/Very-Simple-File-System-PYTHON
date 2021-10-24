import unittest
import VSFS

class TestStringMethods(unittest.TestCase):

    def test_list(self):
        self.assertEqual(VSFS.list_files(['VSFS', 'list', 'FS'], False), '''@Goals
            @CopyFromOutTest
            @now
            @Goals
            =newDirTest/
            =newDir/
            @spaceTest
            
            >''')

    def test_list_error(self):
        self.assertEqual(VSFS.list_files(['VSFS', 'list'], False), 'Invalid list command.')

    def rm_file_not_exist_err(self):
        self.assertEqual(VSFS.list_files(['VSFS', 'rm', 'FS', 'asdasd'], False), 'File not found.')

    def inalid_rm_cmd(self):
        self.assertEqual(VSFS.list_files(['VSFS', 'rm', 'games'], False), 'Invalid remove command.')


if __name__ == '__main__':
    unittest.main()