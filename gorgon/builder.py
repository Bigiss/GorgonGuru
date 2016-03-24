import codecs
import datetime
import logging
import os
import re

from mako.lookup import TemplateLookup
from mako.template import Template

from gorgon import calculator, json_parser


def html(func):
    """A decorator to wrap fuctions that output HTML."""

    def f(*args, **kwargs):
        (builder,) = args
        header = Template(filename="templates/header.mako").render(
            home_location="/", items_location="/items.html",
            skills_location="/skills.html",
            powers_location="/powers.html",
            recipes_location="/recipes.html",
            abilities_location="/abilities.html",
            simulator_location="/simulator.html",
            parser=builder.parser,
            lastupdate=datetime.datetime.now().strftime("%Y-%m-%d"),
            version_pairs=builder.FindVersionPairs())
        footer = Template(filename="templates/footer.mako").render()
        return header + func(*args, **kwargs) + footer

    return f


class Builder(object):
    def __init__(self, parser):
        self.parser = parser
        self.calculator = calculator.Calculator(parser)
        self.template_lookup = TemplateLookup(".")

    def Template(self, filename):
        return Template(filename=filename, lookup=self.template_lookup)

    @html
    def IndexReport(self):
        return self.Template("templates/index.mako").render()

    @html
    def ItemsReport(self):
        return self.Template("templates/items_page.mako").render(items=self.parser.items.values())

    def DumpItemKeys(self, directory):
        key2field = {
            "Keyword": "keywords",
            "EquipmentSlot": "slot",
        }
        print "Dumping itemkeys to directory: %s" % directory
        try:
            os.makedirs(directory)
        except OSError:
            pass

        for item_key in self.parser.item_keys:
            field, value = item_key.split(":")
            item_field = key2field.get(field)
            if not item_field:
                continue

            filtered_items = []
            for item in self.parser.items.values():
                item_field = getattr(item, key2field.get(field)) or []
                if value in item_field:
                    filtered_items.append(item)
                elif any([x.startswith(value+"=") for x in item_field]):
                    filtered_items.append(item)
            filtered_items = sorted(filtered_items, key=lambda x:x.name)
            with codecs.open(os.path.join(directory, "items_%s.html" % item_key), "wb", encoding="utf-8") as fd:
                fd.write(self.Template("templates/items_tiny.mako").render(items=filtered_items))

    @html
    def RecipesReport(self):
        return self.Template("templates/recipes_page.mako").render(recipes=self.parser.recipes.values())

    @html
    def PowersReport(self):
        return self.Template("templates/powers_page.mako").render(powers=self.parser.powers.values())

    def DumpSkills(self, directory):
        print "Dumping skills to directory: %s" % directory
        try:
            os.makedirs(directory)
        except OSError:
            pass

        for skill in self.parser.skills.values():
            if not skill.id:
                continue

            with codecs.open(os.path.join(directory, "%d.html" % skill.id), "wb", encoding="utf-8") as fd:
                skill_page = self.Template("templates/skill_page.mako").render(
                        skill=skill, skills=self.parser.skills, abilities=self.parser.abilities.values(),
                        recipes=self.parser.recipes.values())
                content = html(lambda x:skill_page)(self)
                fd.write(content)

    @html
    def AbilitiesReport(self):
        ability_data = []
        for name, ability in sorted(self.parser.abilities.iteritems(), key=lambda x: x[1].skill):
            min_, avg, pct, max_ = self.calculator.CalculateDamage(name)
            adpp = ""
            if avg and ability.power_cost:
                adpp = "%.0f" % (avg / ability.power_cost)

            if min_:
                min_ = "%d" % min_
            else:
                min_ = ""

            if avg:
                avg = "%d" % avg
                pct = "%.0f%%" % (pct * 100)
            else:
                avg = pct = ""

            if max_:
                max_ = "%d" % max_
            else:
                max_ = ""

            percent_mods = []
            for skill_base, chance, source in ability.mods["SkillBase"]:
                if chance < 1.0:
                    percent_mods.append(
                            '<span title="%s">%d%% (%d%%)</span>' % (source, skill_base * 100, chance * 100))
                else:
                    percent_mods.append('<span title="%s">%d%%</span>' % (source, skill_base * 100))

            flat_mods = []
            for flat_bonus, flat_chance, source in ability.mods["SkillFlat"]:
                if flat_chance < 1.0:
                    flat_mods.append(
                            '<span title="%s">%d (%d%%)</span>' % (source, flat_bonus, flat_chance * 100))
                else:
                    flat_mods.append('<span title="%s">%d</span>' % (source, flat_bonus))

            ability_data.append((ability, min_, avg, pct, max_, percent_mods, flat_mods, adpp))
        return self.Template("templates/abilities_page.mako").render(abilities=ability_data)

    def DumpItems(self, directory):
        print "Dumping items to directory: %s" % directory
        try:
            os.makedirs(directory)
        except OSError:
            pass

        for item in self.parser.items.values():
            if not item.id:
                continue

            with codecs.open(os.path.join(directory, "item_%d.html" % item.id), "wb", encoding="utf-8") as fd:
                fd.write(self.Template("templates/item_tooltip.mako").render(item=item))

    def ChangesReport(self, directory):
        self.changes_directory = directory
        try:
            os.makedirs(directory)
        except OSError:
            pass

        for v1, v2 in self.FindVersionPairs():
            logging.info("Building %s vs %s", v1, v2)
            prev_version = json_parser.GorgonJsonParser(v1)
            prev_version.Parse("data")
            next_version = json_parser.GorgonJsonParser(v2)
            next_version.Parse("data")
            differences, changes = next_version - prev_version

            with codecs.open(os.path.join(directory, "%d_to_%d.html" % (v1, v2)), "wb", encoding="utf-8") as fd:
                changes_page = self.Template("templates/changes_template.mako").render(
                    old_version=v1, new_version=v2,
                    items=differences.items.values(),
                    abilities=differences.abilities.values(),
                    skills=differences.skills.values(),
                    powers=differences.powers.values(),
                    recipes=differences.recipes.values(),
                    changes=changes)
                fd.write(html(lambda x:changes_page)(self))

    @html
    def BuilderReport(self):
        return self.Template("templates/simulator_page.mako").render()

    def GeneratedPowersReport(self):
        return self.Template("templates/generated_powers.mako").render(powers=self.parser.powers)

    def BuilderJavascriptReport(self):
        return self.Template("templates/builder.js").render()

    def FindVersionPairs(self):
        root, versions, _ = os.walk(self.parser.data_directory).next()
        versions = sorted(filter(lambda x:re.match("v[0-9]+", x), versions))
        for v1, v2 in zip(versions[::-1][1:], versions[::-1][:-1]):
            yield int(v1[1:]), int(v2[1:])
