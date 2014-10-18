from unittest import TestCase
from pydic import Parameters


class ParametersTestCase(TestCase):
    def test_get(self):
        parameters = Parameters({'foo': 'bar', 'hello': 'world'})
        self.assertEqual('bar', parameters.get('foo'))
        self.assertEqual('world', parameters.get('hello'))
        self.assertEqual('bbb', parameters.get('aaa', 'bbb'))

    def test_get_parameter_which_references_other_parameter(self):
        parameters = Parameters({'name': 'Felix', 'hello_message': 'Hi {{ name }}!'})
        self.assertEqual('Hi Felix!', parameters.get('hello_message'))

    def test_set(self):
        parameters = Parameters({'foo': 'bar', 'hello': 'world'})
        parameters.set('foo', 'abc')
        self.assertTrue('abc', parameters.get('foo'))

    def test_has(self):
        parameters = Parameters({'foo': 'bar', 'hello': 'world'})
        self.assertTrue(parameters.has('foo'))
        self.assertFalse(parameters.has('another'))
        self.assertTrue(parameters.has('hello'))

    def test_all(self):
        params = {'foo': 'bar', 'hello': 'world'}
        parameters = Parameters(params)
        self.assertEqual(parameters.all(), params)

    def test_add(self):
        parameters = Parameters({'foo': 'bar'})
        parameters.add({'hello': 'world', 'bbb': 222})
        self.assertEqual('bar', parameters.get('foo'))
        self.assertEqual('world', parameters.get('hello'))
        self.assertEqual(222, parameters.get('bbb'))

    def test_remove(self):
        parameters = Parameters({'foo': 'bar', 'hello': 'world', 'aaa': 111})
        parameters.remove('hello')
        self.assertEqual({'foo': 'bar', 'aaa': 111}, parameters.all())

    def test_keys(self):
        parameters = Parameters({'foo': 'bar', 'hello': 'world'})
        keys = parameters.keys()
        self.assertTrue('foo' in keys)
        self.assertTrue('hello' in keys)

    def test_count(self):
        parameters = Parameters({'foo': 'bar', 'hello': 'world', 'aaa': 111})
        self.assertEqual(3, parameters.count())
