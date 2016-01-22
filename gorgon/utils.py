import re


def myescape(text):
    return text.replace(u"\n", u'<br>').replace(u'"', u'\\"')


def itemlink(item):
    item_name = getattr(item, "name", item)
    item_id = getattr(item, "id", 0)
    return u'<a class="itemtooltip" rel="items/item_%d.html">%s</a>' % (item_id, item_name)


def build_ingredient(ingredient):
    return "%d %s" % (ingredient[0], itemlink(ingredient[1]))


def colorize(text):
    def colorizer(matchobj):
        return u'<span class="highlight">%s</span>' % matchobj.group(0)

    return re.sub("([0-9]+%?)", colorizer, text)
