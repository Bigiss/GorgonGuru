import re

from gorgon import model


def myescape(text):
    return text.replace(u"\n", u'<br>').replace(u'"', u'\\"')


def itemlink(item):
    item_name = getattr(item, "name", item)
    item_id = getattr(item, "id", 0)
    if isinstance(item, model.Item):
        if item.sellers:
            return u'<a class="itemtooltip soldbymerchant" rel="/items/item_%d.html">%s</a>' % (item_id, item_name)
        return u'<a class="itemtooltip" rel="/items/item_%d.html">%s</a>' % (item_id, item_name)
    elif isinstance(item, model.ItemFilter):
        return u'<a class="itemtooltip itemfilter" rel="/itemkeys/items_%s.html" href="/items.html#%s">%s</a>' % (item.KeysFilter(), item.KeysFilter(), item.desc)


def build_ingredient(ingredient, with_image=False, hidden=False):
    if with_image:
        return "%s %d %s" % (ingredient[1].RenderIcon(hidden=hidden), ingredient[0], itemlink(ingredient[1]))
    return "%d %s" % (ingredient[0], itemlink(ingredient[1]))


def colorize(text):
    def colorizer(matchobj):
        return u'<span class="highlight">%s</span>' % matchobj.group(0)

    return re.sub("([0-9]+%?)", colorizer, text)
