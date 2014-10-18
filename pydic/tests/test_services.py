from unittest import TestCase
from pydic import Services, ServicesException, Parameters


class SimpleService:
    def __init__(self):
        pass

    def say(self):
        return 'hello'


class SimpleServiceWithConstructorArguments:
    def __init__(self, name, surname):
        self._name = name
        self._surname = surname

    def say(self):
        return 'hello %s %s' % (self._name, self._surname)


class SimpleServiceWithCallsWithArguments:
    def __init__(self):
        self._name = None
        self._surname = None

    def set_name(self, name):
        self._name = name

    def set_surname(self, surname):
        self._surname = surname

    def say(self):
        return 'hello %s %s' % (self._name, self._surname)


class SimpleServiceWithCallWithArguments:
    def __init__(self):
        self._name = None
        self._surname = None

    def set_name_surname(self, name, surname):
        self._name = name
        self._surname = surname

    def say(self):
        return 'hello %s %s' % (self._name, self._surname)


class SimpleServiceWithCallsWithoutArguments:
    def __init__(self):
        self._name = None
        self._surname = None

    def set_name(self):
        self._name = 'Felix'

    def set_surname(self):
        self._surname = 'Carmona'

    def say(self):
        return 'hello %s %s' % (self._name, self._surname)


class CarService:
    def __init__(self, driver):
        self._driver = driver

    def drive(self):
        return '%s is driving' % self._driver.get_name()


class DriverService:
    def __init__(self, name):
        self._name = name

    def get_name(self):
        return self._name


class ServicesTestCase(TestCase):
    def test_get_most_simple_service(self):
        definitions = {
            'simple': {
                'class': 'pydic.tests.test_services.SimpleService'
            }
        }
        services = Services(definitions)
        service = services.get('simple')
        self.assertEqual('hello', service.say())
        same_service = services.get('simple')
        self.assertTrue(service is same_service)

    def test_fail_when_tries_to_get_an_unknown_service(self):
        services = Services({})
        self.assertRaises(ServicesException, services.get, 'unknown_service')

    def test_service_definition_referencing_other_service_definition(self):
        definitions = {
            'simple': {
                'class': 'pydic.tests.test_services.SimpleService'
            },
            'alias_of_service': '@simple'
        }
        services = Services(definitions)
        service = services.get('alias_of_service')
        self.assertEqual('hello', service.say())
        same_service = services.get('simple')
        self.assertTrue(service is same_service)

    def test_escape_service(self):
        definitions = {
            'simple': {
                'class': 'pydic.tests.test_services.SimpleServiceWithConstructorArguments',
                'arguments': {
                    'name': '@@foo',
                    'surname': 'abc'
                }
            }
        }

        services = Services(definitions)
        service = services.get('simple')
        self.assertEqual('hello @foo abc', service.say())

    def test_escape_parameter(self):
        definitions = {
            'simple': {
                'class': 'pydic.tests.test_services.SimpleServiceWithConstructorArguments',
                'arguments': {
                    'name': "\{\{ foo \}\} {{ surname }}",
                    'surname': 'abc'
                }
            }
        }
        parameters = {
            'surname': 'Carmona'
        }

        services = Services(definitions, Parameters(parameters))
        service = services.get('simple')
        self.assertEqual('hello {{ foo }} Carmona abc', service.say())

    def test_service_definition_with_parameter_argument(self):
        definitions = {
            'simple': {
                'class': 'pydic.tests.test_services.SimpleServiceWithConstructorArguments',
                'arguments': {
                    'name': '{{ my_user_name }}',
                    'surname': '{{ my_user_surname }}xxx'
                }
            }
        }

        parameters = Parameters({'my_user_name': 'Felix', 'my_user_surname': 'Carmona'})
        services = Services(definitions, parameters)
        service = services.get('simple')
        self.assertEqual('hello Felix Carmonaxxx', service.say())

    def test_fail_when_tries_to_get_a_malformed_definition(self):
        definitions = {
            'simple': {
                'xxx': 'aaa'
            }
        }
        services = Services(definitions)
        self.assertRaises(ServicesException, services.get, 'simple')

    def test_service_with_constructor_arguments_as_dict(self):
        definitions = {
            'simple': {
                'class': 'pydic.tests.test_services.SimpleServiceWithConstructorArguments',
                'arguments': {
                    'name': 'Felix',
                    'surname': 'Carmona'
                }
            }
        }
        services = Services(definitions)
        service = services.get('simple')
        self.assertEqual('hello Felix Carmona', service.say())

    def test_service_with_constructor_arguments_as_list(self):
        definitions = {
            'simple': {
                'class': 'pydic.tests.test_services.SimpleServiceWithConstructorArguments',
                'arguments': ['Felix', 'Carmona']
            }
        }
        services = Services(definitions)
        service = services.get('simple')
        self.assertEqual('hello Felix Carmona', service.say())

    def test_fail_when_definition_arguments_are_not_dict_or_tuple_or_list(self):
        definitions = {
            'simple': {
                'class': 'pydic.tests.test_services.SimpleServiceWithConstructorArguments',
                'arguments': 'Felix'
            }
        }
        services = Services(definitions)
        self.assertRaises(ServicesException, services.get, 'simple')

    def test_service_with_calls_with_arguments_as_list(self):
        definitions = {
            'simple': {
                'class': 'pydic.tests.test_services.SimpleServiceWithCallsWithArguments',
                'calls': [
                    ['set_name', ['Felix']],
                    ['set_surname', ['Carmona']]
                ]
            }
        }
        services = Services(definitions)
        service = services.get('simple')
        self.assertEqual('hello Felix Carmona', service.say())

    def test_service_with_calls_with_arguments_as_dict(self):
        definitions = {
            'simple': {
                'class': 'pydic.tests.test_services.SimpleServiceWithCallWithArguments',
                'calls': [
                    ['set_name_surname', {'surname': 'Carmona', 'name': 'Felix'}]
                ]
            }
        }
        services = Services(definitions)
        service = services.get('simple')
        self.assertEqual('hello Felix Carmona', service.say())

    def test_service_with_calls_without_arguments(self):
        definitions = {
            'simple': {
                'class': 'pydic.tests.test_services.SimpleServiceWithCallsWithoutArguments',
                'calls': [
                    'set_name',
                    'set_surname'
                ]
            }
        }
        services = Services(definitions)
        service = services.get('simple')
        self.assertEqual('hello Felix Carmona', service.say())

    def test_service_with_sub_dependency(self):
        definitions = {
            'car': {
                'class': 'pydic.tests.test_services.CarService',
                'arguments': ['@driver']
            },
            'driver': {
                'class': 'pydic.tests.test_services.DriverService',
                'arguments': ['{{ driver_name }}']
            }
        }
        parameters = Parameters({'driver_name': 'Felix'})
        services = Services(definitions, parameters)
        service = services.get('car')
        self.assertEqual('Felix is driving', service.drive())

    def test_fail_when_call_function_arguments_are_malformed(self):
        definitions = {
            'simple': {
                'class': 'pydic.tests.test_services.SimpleServiceWithCallWithArguments',
                'calls': [
                    ['set_name_surname', 1]
                ]
            }
        }
        services = Services(definitions)
        self.assertRaises(ServicesException, services.get, 'simple')

    def test_fail_when_call_function_not_exists_in_service(self):
        definitions = {
            'simple': {
                'class': 'pydic.tests.test_services.SimpleServiceWithCallsWithoutArguments',
                'calls': [
                    'set_namex'
                ]
            }
        }
        services = Services(definitions)
        self.assertRaises(ServicesException, services.get, 'simple')

    def test_set_service(self):
        simple = SimpleService()
        services = Services()
        services.set('simple', simple)
        same_simple = services.get('simple')
        self.assertEqual('hello', same_simple.say())

    def test_has_service(self):
        definitions = {
            'simple': {
                'class': 'pydic.tests.test_services.SimpleService'
            }
        }
        services = Services(definitions)
        self.assertTrue(services.has('simple'))
        self.assertFalse(services.has('foo_service'))

    def test_remove_service(self):
        definitions = {
            'simple': {
                'class': 'pydic.tests.test_services.SimpleService'
            }
        }
        services = Services(definitions)
        services.get('simple')
        services.remove('simple')
        self.assertFalse(services.has('simple'))

    def test_add_services(self):
        definitions = {
            'simple': {
                'class': 'pydic.tests.test_services.SimpleService'
            }
        }
        services = Services(definitions)
        services.add({'new_service_one': SimpleService(), 'new_service_two': SimpleService()})
        self.assertTrue(services.has('simple'))
        self.assertTrue(services.has('new_service_one'))
        self.assertTrue(services.has('new_service_two'))

    def test_get_keys_services(self):
        definitions = {
            'simple': {
                'class': 'pydic.tests.test_services.SimpleService'
            },
            'other': {
                'class': 'pydic.tests.test_services.SimpleService'
            }
        }
        services = Services(definitions)
        services.add({'new_service_one': SimpleService(), 'new_service_two': SimpleService()})
        expected = ['other', 'simple', 'new_service_one', 'new_service_two']
        actual = services.keys()
        self.assertEqual(set(expected), set(actual))