#!/usr/bin/python3
""" tests for the console module """
from console import HBNBCommand
from models import storage
import unittest
from unittest.mock import patch
from io import StringIO
import os


class testConsole(unittest.TestCase):
    """ test class for console """
    def setUp(self):
        """ set up the test class """
        self.hbnbCmd = HBNBCommand()
        self.prev_filestorage_file_path = storage._FileStorage__file_path
        storage._FileStorage__file_path = "test_file.json"
        try:
            os.remove("test_file.json")
        except FileNotFoundError:
            pass
        self.classes = ["BaseModel", "User", "Place", "State",
                        "City", "Amenity", "Review"]

    def tearDown(self):
        """ clean up the test class """
        storage._FileStorage__file_path = self.prev_filestorage_file_path
        try:
            os.remove("test_file.json")
        except FileNotFoundError:
            pass

    def test_create(self):
        """ test the create command of the console """
        for obj_idx, cls in enumerate(self.classes):
            with patch('sys.stdout', new=StringIO()) as f:
                self.hbnbCmd.onecmd("create {}".format(cls))
            self.assertEqual(obj_idx + 1, len(storage.all()))
            obj_id = f.getvalue()[:-1]
            key = "{}.{}".format(cls, obj_id)
            self.assertEqual(obj_id, storage.all()[key].id)

    def test_create_with_params(self):
        """ test the create command with parameters """
        with patch('sys.stdout', new=StringIO()) as f:
            self.hbnbCmd.onecmd('create User name="john" \
                                            email="john@hbnb.com" \
                                            password="johndoe" \
                                            age=20 \
                                            height=175.4 \
                                            greeting="hello!_i\'m_john!"')
        obj_id = f.getvalue()[:-1]
        key = "User.{}".format(obj_id)
        obj = storage.all()[key]
        self.assertEqual(obj_id, obj.id)
        self.assertEqual(getattr(obj, "name"), "john")
        self.assertEqual(getattr(obj, "email"), "john@hbnb.com")
        self.assertEqual(getattr(obj, "password"), "johndoe")
        self.assertEqual(getattr(obj, "age"), 20)
        self.assertEqual(getattr(obj, "height"), 175.4)
        self.assertEqual(getattr(obj, "greeting"), "hello! i'm john!")
        with patch('sys.stdout', new=StringIO()) as f:
            self.hbnbCmd.onecmd('show User {}'.format(obj_id))
        obj_repr = f.getvalue()[:-1]
        self.assertEqual(obj_repr, obj.__str__())

        with patch('sys.stdout', new=StringIO()) as f:
            self.hbnbCmd.onecmd('create City name="Lagos" \
                                            slogan="\\"Eko_o_ni_baje!\\"" \
                                            weather = calm')
        obj_id = f.getvalue()[:-1]
        key = "City.{}".format(obj_id)
        obj = storage.all()[key]
        self.assertEqual(obj_id, obj.id)
        self.assertEqual(getattr(obj, "name"), "Lagos")
        self.assertEqual(getattr(obj, "slogan"), '"Eko o ni baje!"')
        with patch('sys.stdout', new=StringIO()) as f:
            self.hbnbCmd.onecmd('show City {}'.format(obj_id))
        obj_repr = f.getvalue()[:-1]
        self.assertEqual(obj_repr, obj.__str__())
