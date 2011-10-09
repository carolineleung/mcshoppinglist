from unittest.case import TestCase
from mcshoppinglist.shared.exceptions import ShoppingListError

class ShoppingListExceptionTest(TestCase):
    EXPECTED_MESSAGE1 = 'Expected message 1'
    EXPECTED_MESSAGE2 = 'Expected message 2'
    EXPECTED_MESSAGE3 = 'Expected message 3'

    def test_message(self):
        try:
            raise ShoppingListError(ShoppingListExceptionTest.EXPECTED_MESSAGE1)
        except Exception as ex:
            self.assertEquals(ShoppingListExceptionTest.EXPECTED_MESSAGE1, ex.message)

    def test_rethrow(self):
        try:
            try:
                try:
                    raise ShoppingListError(ShoppingListExceptionTest.EXPECTED_MESSAGE1)
                except Exception as ex3:
                    raise ShoppingListError(ShoppingListExceptionTest.EXPECTED_MESSAGE2, ex3)
            except Exception as ex2:
                raise ShoppingListError(ShoppingListExceptionTest.EXPECTED_MESSAGE3, ex2)
        except ShoppingListError as ex:
            self.assertEquals(ShoppingListExceptionTest.EXPECTED_MESSAGE3, ex.message)
            self.assertEquals(ShoppingListExceptionTest.EXPECTED_MESSAGE2, ex.inner_exception.message)
            self.assertEquals(ShoppingListExceptionTest.EXPECTED_MESSAGE1, ex.inner_exception.inner_exception.message)
            print ex.traceback_str
            self.assertTrue(len(ex.traceback_str) > 0)