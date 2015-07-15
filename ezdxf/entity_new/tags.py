import collections

Tag = collections.namedtuple("DXFTag", "key value")


class TagContainer(list):
    # todo: remove
    def __contains__(self, key):
        return any([tag.key == key for tag in self]) or super(TagContainer, self).__contains__(key)

    def remove(self, key):
        if not isinstance(key, Tag):
            removed = []
            for index in self.iter_tags(key):
                removed.append(self.pop(index))
            return removed
        print(key)
        return super(TagContainer, self).remove(key)

    def iter_tags(self, key):
        """
        get all tags positions for a given key
        """
        for index, tag in enumerate(self):
            if tag.key == key:
                yield index

    def get_tag_groups(self, key):
        """
        Iterate over a sequence, starting from given key till next appearance
        """
        tags = self.iter_tags(key)
        groups = []

        start = next(tags, 0)
        for stop in tags:
            if stop > start:
                subcontainer = self.__class__(self[start:stop])
                groups.append(subcontainer)
                start = stop

        if groups:
            subcontainer = self.__class__(self[start:])
            groups.append(subcontainer)

        return groups







    @property
    def subclasses(self):
        # code 100
        return [0]

    def insert(self, values, subclass=0):
        index = self.subclasses[subclass]
        #self._tags.insert(values, index)
        self += values