class SchemaEntity(dict):
    """
    Base class, extends dict, so we can use objects as dictionaries, but this also
    enables json support ootb (Without custom serialisation methods.


    Here we add the '_type' or 'event' properties, so we can json serialize, without losing
    info on what kind of object it was
    """
    def __init__(self, **kwargs):
        dict.__init__(self, **kwargs)

        if hasattr(self, '_type'):
            self['_type'] = self._type
        else:
            # this should never happen! But better safe than sorry
            raise Exception(f'Unknown entity / missing attributes in {type(self)}')

        # if we don't know our ancestry, we populate it here
        if not hasattr(self, '_types'):
            self._types = self._get_types()
            self['_types'] = self._types

    @staticmethod
    def _get_parents(cls, parents: list = None):
        if not parents:
            parents = []
        parents.insert(0, cls.__name__)
        # we recursively infer the class hierharchy, but we are not interested going further than AbstractContext
        # or AbstractEvent whose parent is SchemaEntity
        if cls.__base__ and cls.__base__ != SchemaEntity:
            SchemaEntity._get_parents(cls.__base__, parents)

        return parents

    @classmethod
    def _get_types(cls, parents: list = None) -> list:
        return SchemaEntity._get_parents(cls)

    def __getattr__(self, item):
        """
        wrapper to allow attribute access to dictionary values by key
        :param item:
        :return:
        """
        try:
            return self[item]
        except KeyError:
            raise AttributeError
