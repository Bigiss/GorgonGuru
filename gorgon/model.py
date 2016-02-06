import logging

from mako.template import Template


class IconMixin(object):
    """A mixin to be able to render icons."""
    def __init__(self, *args, **kwargs):
        super(IconMixin, self).__init__(*args, **kwargs)

    def RenderIcon(self, hidden=False, height=32, width=32):
        if self.icon:
            if hidden:
                template = Template(u"<img class=\"loading\" orig=\"http://cdn.projectgorgon.com/v${version}/icons/icon_${iconid}.png\" width=\"%d\" height=\"%d\">" % (width, height))
            else:
                template = Template(u"<img src=\"http://cdn.projectgorgon.com/v${version}/icons/icon_${iconid}.png\" width=\"%d\" height=\"%d\">" % (width, height))
            return template.render(version=self.version, iconid=self.icon or "unknown")


class BaseGorgonObject(object):
    """Base class for all Gorgon objects."""

    def __init__(self, **kwargs):
        super(BaseGorgonObject, self).__setattr__('_attributes', {})
        self._attributes.update(kwargs)
        self.keywords = kwargs.get('keywords', [])

    def __getattr__(self, item):
        return self._attributes.get(item, None)

    def __setattr__(self, key, value):
        self._attributes[key] = value

    def __unicode__(self):
        return unicode(self.name) or repr(self)

    def __str__(self):
        return str(self.name) or repr(self)

    def __eq__(self, other):
        return all([getattr(self, attr, None) == getattr(other, attr, None) for attr in self._attributes])

    def Differences(self, other):
        diffs = {}
        for attr_name, attr_value in self._attributes.iteritems():
            if attr_name in ("version", "sellers", "keywords", "mods"):
                continue
            other_value = getattr(other, attr_name, None)
            if attr_value != other_value:
                diffs[attr_name] = [other_value, attr_value]
        return diffs


class Item(BaseGorgonObject, IconMixin):
    """Base class for all Gorgon items."""

    def __init__(self, **kwargs):
        super(Item, self).__init__(**kwargs)
        self.effects = kwargs.get('effects', [])
        self.keywords = kwargs.get('keywords', [])
        self.stack_size = kwargs.get('stack_size', 1)
        self.sellers = kwargs.get('sellers', [])

    def __unicode__(self):
        return u"%s (%dc): '%s'" % (self.name, self.value, self.description)


class Recipe(BaseGorgonObject, IconMixin):
    pass


class Ability(BaseGorgonObject, IconMixin):
    def __init__(self, **kwargs):
        super(Ability, self).__init__(**kwargs)
        self.skill = kwargs.get('skill', 'Unknown')
        self.textual_mods = kwargs.get("mods")
        self.mods = kwargs.get('mods', dict(SkillBase=[], SkillFlat=[]))


class Skill(BaseGorgonObject):
    def __init__(self, **kwargs):
        super(Skill, self).__init__(**kwargs)
        self.combat = kwargs.get('combat', False)
        self.crafting = kwargs.get('crafting', False)
        self.foraging = kwargs.get('foraging', False)
        self.rewards = kwargs.get('rewards', {})
        self.parents = kwargs.get('parents', {})
        self.subskills = kwargs.get('subskills', [])

    def __unicode__(self):
        return unicode(self.name)

    def __str__(self):
        return str(self.name)


class Attribute(BaseGorgonObject):
    def __init__(self, **kwargs):
        super(Attribute, self).__init__(**kwargs)
        self.is_hidden = kwargs.get('is_hidden', False)

    def __unicode__(self):
        return self.label

    def __str__(self):
        return str(self.label)


class Merchant(BaseGorgonObject):
    def __init__(self, **kwargs):
        super(Merchant, self).__init__(**kwargs)
        self.sales = kwargs.get('sales', [])

    def Item(self, item):
        return self.sales[item]


class ShopItem(BaseGorgonObject):
    def __init__(self, **kwargs):
        super(ShopItem, self).__init__(**kwargs)
        self.multiple = kwargs.get('multiple', 1)


class Power(BaseGorgonObject):
    def __init__(self, **kwargs):
        super(Power, self).__init__(**kwargs)
        self.slots = kwargs.get("slots", ["??"])
        self.tiers = kwargs.get("tiers", {})

class ItemFilter(BaseGorgonObject):
    """Represents a list of items by a filter."""
    def __init__(self, **kwargs):
        super(ItemFilter, self).__init__(**kwargs)
        self._items_computed = False
        self._items = False

    def Keys(self):
        for key in self.keys:
            key_category = None
            try:
                key_category, key_value = key.split(":")
            except ValueError:
                try:
                    key_value = key.split(":")
                    key_category = u"Keyword"
                except ValueError:
                    logging.error("Found item key %s. Don't know how toparse.", key)
                    import ipdb;ipdb.set_trace()
            if isinstance(key_value, list):
                yield key_category, u" ".join(key_value)
            else:
                yield key_category, key_value

    def KeysFilter(self):
        return u"&".join([u"%s:%s" % (k, v) for k, v in self.Keys()])

    def Items(self, parser):
        if self._items.parsed:
            return self._items

        self._items = []
        for item in self.parser.items.values():
            matches = True
            # Filter the item by the item filters
            for category, value in self.Keys():
                if category == "Keyword":
                    if value not in item.keywords:
                        matches = False
                        break
                elif category == "EquipmentSlot":
                    if value != item.slot:
                        break
                else:
                    # Don't match cause we don't know how
                    matches = False

            if not matches:
                continue

            self._items.append(item)

    def RenderIcon(self, *args, **kwargs):
        return u""

class Effect(BaseGorgonObject):
    pass