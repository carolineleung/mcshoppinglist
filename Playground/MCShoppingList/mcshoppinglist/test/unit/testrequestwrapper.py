import time
from unittest.case import TestCase
from webob.request import Request
from webob.response import Response
from mcshoppinglist.api.apierrors import JsonErrorFactory
from mcshoppinglist.shared.exceptions import ShoppingListError
from mcshoppinglist.shared.handlerwrapper import RequestHandlerWrapper
from mcshoppinglist.shared.helpers import JsonHelper

class RequestHandlerWrapperTest(TestCase):
    EXPECTED_VALUE = 42

    @staticmethod
    def _fake_handler_static():
        return RequestHandlerWrapperTest.EXPECTED_VALUE

    def _fake_handler_instance(self):
        return RequestHandlerWrapperTest.EXPECTED_VALUE

    def _fake_handler_instance_args(self, arg1, arg2):
        self.assertEqual('arg1value', arg1)
        self.assertEqual('arg2value', arg2)
        return RequestHandlerWrapperTest.EXPECTED_VALUE

    def _fake_handler_raise(self):
        raise Exception('Expected this error.')

    def _fake_handler_raise_with_traceback(self):
        try:
            raise ShoppingListError('Expected this error with traceback 1.')
        except Exception as ex:
            raise ShoppingListError('Expected this error 2.', ex)

    def _create_empty_request(self):
        return {}

    def test_wrapper(self):
        request = self._create_empty_request()
        actual_value = RequestHandlerWrapper.handle(RequestHandlerWrapperTest._fake_handler_static, request)
        self.assertEqual(RequestHandlerWrapperTest.EXPECTED_VALUE, actual_value)
        actual_value = RequestHandlerWrapper.handle(self._fake_handler_instance, request)
        self.assertEqual(RequestHandlerWrapperTest.EXPECTED_VALUE, actual_value)
        actual_value = RequestHandlerWrapper.handle(self._fake_handler_instance_args, 'arg1value', 'arg2value')
        self.assertEqual(RequestHandlerWrapperTest.EXPECTED_VALUE, actual_value)

    def test_wrapper_exceptions(self):
        request = self._create_empty_request()
        actual_value = RequestHandlerWrapper.handle(self._fake_handler_raise, request)
        self.assertTrue(issubclass(actual_value.__class__, Response))
        json_obj_dict = JsonHelper.deserialize_from_json(actual_value.body)
        self.assertTrue(JsonErrorFactory.MESSAGE_KEY in json_obj_dict)
        self.assertTrue(JsonErrorFactory.CODE_KEY in json_obj_dict)

    def test_wrapper_exceptions(self):
        request = self._create_empty_request()
        actual_value = RequestHandlerWrapper.handle(self._fake_handler_raise_with_traceback, request)
        self.assertTrue(issubclass(actual_value.__class__, Response))
        print actual_value.body
        json_obj_dict = JsonHelper.deserialize_from_json(actual_value.body)
        self.assertTrue(JsonErrorFactory.MESSAGE_KEY in json_obj_dict)
        self.assertTrue(JsonErrorFactory.CODE_KEY in json_obj_dict)
        trace_deep = json_obj_dict[JsonErrorFactory.TRACE_DEEP_KEY]
        self.assertTrue(trace_deep.lower().find('file') >= 0, 'Missing traceback.')
        trace_shallow = json_obj_dict[JsonErrorFactory.TRACE_SHALLOW_KEY]
        self.assertTrue(trace_shallow.lower().find('file') >= 0, 'Missing traceback.')

    def test_sleep(self):
        a = 1
        a += 1
        time.sleep(15)
        a += 1

