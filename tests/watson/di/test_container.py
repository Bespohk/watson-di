# -*- coding: utf-8 -*-
from pytest import raises
from watson.di.container import IocContainer
from watson.di import exceptions
from tests.watson.di.support import SampleDependency


class TestIoc(object):

    def test_create_container(self):
        container = IocContainer()
        assert repr(
            container) == '<watson.di.container.IocContainer: 0 param(s), 0 definition(s)>'
        assert container.params == {}
        assert container.definitions == {}

    def test_get_item(self):
        container = IocContainer({
            'definitions': {
                'test': {
                    'item': 'tests.watson.di.support.SampleDependency',
                    'type': 'singleton',
                },
                'test2': {
                    'item': 'tests.watson.di.support.sample_dependency',
                    'type': 'singleton',
                },
                'test3': {
                    'item': 'tests.watson.di.support.sample_dependency_with_args',
                    'type': 'singleton',
                    'init': {
                        'arg': 'some arg'
                    }
                }
            }
        })
        container.add_definition('def', {'item': lambda container: 'something'})
        assert isinstance(container.get('test'), SampleDependency)
        assert container.get('test2') == 'test'
        assert container.get('def') == 'something'
        assert container.get('def') == 'something'
        assert container.get('def') is container.get('def')
        assert container.get('test3') == 'some arg'
        assert len(container.instantiated) == 4

    def test_get_failed_object(self):
        container = IocContainer()
        with raises(exceptions.NotFoundError):
            container.get('none')
            assert True

    def test_add_definition(self):
        container = IocContainer()
        container.add_definition('dep', {'item': lambda container: 'something'})
        assert container.get('dep') == 'something'

    def test_add_instantiated(self):
        container = IocContainer()
        dep = SampleDependency()
        container.add('dep', dep)
        assert container.get('dep') == dep

    def test_add_dict(self):
        container = IocContainer()
        dep = {'something': 'test'}
        container.add('dep', dep)
        assert container.get('dep') == dep

    def test_not_added(self):
        container = IocContainer()
        assert container.get('tests.watson.di.support.not_added') == 'not added'

    def test_module_not_exist(self):
        container = IocContainer()
        with raises(exceptions.NotFoundError):
            container.get('something.blah')

    def test_get_builtin(self):
        container = IocContainer({
            'definitions': {
                'test': {
                    'item': {'test': 'test'}
                }
            }
        })
        assert isinstance(container.get('test'), dict)

    def test_attach_invalid_processor(self):
        with raises(TypeError):
            container = IocContainer()
            container.attach_processor('event.container.pre', 'test')

    def test_prototype(self):
        container = IocContainer({
            'definitions': {
                'test': {
                    'item': 'tests.watson.di.support.SampleDependency',
                    'type': 'prototype'
                }
            }
        })
        test1 = container.get('test')
        test2 = container.get('test')
        assert test1 != test2

    def test_prototype_add(self):
        container = IocContainer()
        dep = SampleDependency()
        container.add('test', dep)
        assert container.get('test') == dep
        dep2 = SampleDependency()
        container.add('test', dep2)
        assert container.get('test') == dep2

    def test_get_self_defined_object(self):
        container = IocContainer()
        obj = container.get('tests.watson.di.support.DependencyWithDefinition')
        assert obj.the_test() == 'test'
