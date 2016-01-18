from gorgon import calculator
from gorgon import model
from mako.template import Template

import codecs
import json
import itertools
import logging
import re
import os
import sys


def html(func):
  """A decorator to wrap fuctions that output HTML."""
  def f(*args, **kwargs):
    (builder,) = args
    header = Template(filename="templates/header.mako").render(
      home_location="/", items_location="items.html",
      skills_location="skills.html",
      powers_location="powers.html",
      recipes_location="recipes.html",
      abilities_location="abilities.html")
    footer = Template(filename="templates/footer.mako").render()
    return header + func(*args, **kwargs) + footer
  return f


class Builder(object):
  def __init__(self, parser):
    self.parser = parser
    self.calculator = calculator.Calculator(parser)

  @html
  def IndexReport(self):
    return Template(filename="templates/index.mako").render()

  @html
  def ItemsReport(self):
    return Template(filename="templates/item_table.mako").render(items=self.parser.items.values())

  @html
  def RecipesReport(self):
    return Template(filename="templates/recipes_table.mako").render(recipes=self.parser.recipes.values())

  @html
  def PowersReport(self):
    return Template(filename="templates/powers_table.mako").render(powers=self.parser.powers.values())

  @html
  def SkillsReport(self):
    return Template(filename="templates/skills_table.mako").render(skills=self.parser.skills.values())

  @html
  def AbilitiesReport(self):
    ability_data = []
    for name, ability in sorted(self.parser.abilities.iteritems(), key=lambda x:x[1].skill):
      min_, avg, pct, max_ = self.calculator.CalculateDamage(name)
      if min_:
        min_ = "%d" % min_
      else:
        min_ = ""

      if avg:
        avg = "%d" % avg
        pct = "%.0f%%" % (pct*100)
      else:
        avg = pct = ""

      if max_:
        max_ = "%d" % max_
      else:
        max_ = ""

      percent_mods = []
      for skill_base, chance, source in ability.mods["SkillBase"]:
        if chance < 1.0:
          percent_mods.append('<span title="%s">%d%% (%d%%)</span>' % (source, skill_base*100, chance*100))
        else:
          percent_mods.append('<span title="%s">%d%%</span>' % (source, skill_base*100))

      flat_mods = []
      for flat_bonus, flat_chance, source in ability.mods["SkillFlat"]:
        if flat_chance < 1.0:
          flat_mods.append('<span title="%s">%d (%d%%)</span>' % (source, flat_bonus*100, flat_chance*100))
        else:
          flat_mods.append('<span title="%s">%d</span>' % (source, flat_bonus))

      ability_data.append((ability, min_, avg, pct, max_, percent_mods, flat_mods))
    return Template(filename="templates/abilities_table.mako").render(abilities=ability_data)

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
        fd.write(Template(filename="templates/item_tooltip.mako").render(item=item))
