import unittest

from mock import patch

import common
from common import service, api_exception


@patch("common.service.db.find")
class TestService(unittest.TestCase):
    """Test suite for the service layer.
    The underlying find method is mocked in order to not execute the real find
    which queries MongoDB.
    """
    TEST_STRING = "test"
    TEST_FROM = 0
    TEST_TO = 1449107949
    TEST_KEYWORD = "HurrDurr"

    def test_retrieve_items_mandatory_parameters(self, mock_find):
        self.assertRaises(api_exception.BadRequestException,
                          service.retrieve_items, None, self.TEST_FROM,
                          self.TEST_TO)
        self.assertRaises(api_exception.BadRequestException,
                          service.retrieve_items, self.TEST_STRING, None,
                          self.TEST_TO)
        self.assertRaises(api_exception.BadRequestException,
                          service.retrieve_items, self.TEST_STRING,
                          self.TEST_FROM, None)
        self.assertRaises(api_exception.BadRequestException,
                          service.retrieve_items, None, None, None)
        self.assertRaises(api_exception.BadRequestException,
                          service.retrieve_items, None, None, self.TEST_TO)
        self.assertRaises(api_exception.BadRequestException,
                          service.retrieve_items, None, self.TEST_FROM, None)

    def test_retrieve_items_invalid_from_and_to(self, mock_find):
        self.assertRaises(api_exception.BadRequestException,
                          service.retrieve_items, self.TEST_STRING,
                          "I'm not an int", self.TEST_TO)
        self.assertRaises(api_exception.BadRequestException,
                          service.retrieve_items, self.TEST_STRING,
                          self.TEST_FROM, "I'm not an int")

    def test_retrieve_items_valid_parameters(self, mock_find):
        # Call retrieve_items with valid parameters and see if they are
        # correctly passed on to the find method
        common.service.retrieve_items(self.TEST_STRING, self.TEST_FROM, self.TEST_TO,
                                      self.TEST_KEYWORD)
        mock_find.assert_called_once_with(self.TEST_STRING, self.TEST_FROM,
                                     self.TEST_TO, self.TEST_KEYWORD)


if __name__ == '__main__':
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestService)
    unittest.TextTestRunner(verbosity=2).run(test_suite)
