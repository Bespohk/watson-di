Usage
=====

The container is configured via a dict containing the following keys:

params
    A dict of data that can be injected into a dependency. If the value of the key is the same as the name of another dependency then the dependency will be referenced.

definitions
    A dict of definitions that are to be loaded by the container.
    Available keys within a definition are:
        item
            The qualified name of a class or function
        type
            singleton (only load the dependency once) or prototype (instantiate and return a new dependency on each request)
        init
            A list or dict of items to be injected into the dependency on instantiation.
        setter
            A list or dict of methods to be called upon instantiation.
        property:
            A list or dict of methods to be called upon instantiation.

    Only 'item' is a required key.

processors
    A dict of events to be listened for and processors to be called.


.. code-block:: python

    container = IocContainer({
        'params': {
            'db.host': 'localhost'
        },
        'definitions': {
            'database': {
                'item': 'db.adapters.MySQL'
                'init': {
                    'host': 'db.host',
                    'username': 'simon',
                    'password': 'test',
                    'db': 'test'
                }
            }
        }
    })
    db = container.get('database')  # an instance of db.adapters.MySQL
