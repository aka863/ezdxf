import collections

Tag = collections.namedtuple("TAG", "key value")


class Tags():
    def __init__(self, tags=None):
        self._tags = tags or []

    def __iter__(self):
        return self._tags.__iter__()

    def __contains__(self, item):
        return any([tag.key == item for tag in self._tags])

    def remove(self, key):
        self._tags = [tag for tag in self._tags if tag.key != key]

    def get_tags(self, key):
        return [tag for tag in self._tags if tag.key == key]

    @property
    def subclasses(self):
        return [0]

    def insert(self, values, subclass=0):
        index = self.subclasses[subclass]
        #self._tags.insert(values, index)
        self._tags += values