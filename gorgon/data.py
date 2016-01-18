import codecs
import json
import itertools
import logging
import re
import os
import sys


class GorgonJsonParser(object):
  def __init__(self, version):
    self.directory = os.path.join("./", "v%d" % version)
    self.version = version
    self.attributes = dict()
    self.attr_properties = set()
    self.ParseAttributes()
    self.items_properties = set()
    self.items = dict()
    self.ParseItems()
    self.effects = dict()
    self.effects_properties = set()
    self.ParseEffects()
    self.abilities = dict()
    self.abilities_properties = set()
    self.ability2skill = dict()
    self.ParseAbilities()
    self.skills = dict()
    self.skills_properties = set()
    self.ParseSkills()
    self.powers = dict()
    self.powers_properties = set()
    self.ParseTSysClientInfo()
    self.recipes =dict()
    self.recipe_properties = set()
    self.ParseRecipes()

  def _OpenDataFile(self, filename):
    filepath = os.path.join(self.directory, filename)
    return json.load(codecs.open(filepath, "rb", encoding="latin-1"))

  def _ParseEffect(self, effect):
    regexp = ("{(?P<attr>[^}]+)}"
              "{(?P<value>[^}]+)}"
              "{?(?P<restr>[^}]+)?}?")
    matches = re.match(regexp, effect)
    if not matches:
      # This is a standard description
      return effect, None, None

    return matches.group("attr"), matches.group("value"), matches.group("restr")

  def _FormatEffect(self, effect):
      attribute, value, restriction = self._ParseEffect(effect)
      if not value:
        return attribute
      attribute = self.attributes.get(attribute, attribute)
      # Handle % labels
      if attribute.label.endswith("%"):
        return u"%s %+d%%" % (attribute.label[:-1], float(value) * 100)
      try:
        value = int(value)
        return u"%s %+d" % (attribute, value)
      except (TypeError, ValueError):
        return u"%s %s" % (attribute, value)

  def ParseItems(self):
    data = self._OpenDataFile("items.json")

    for item_id, item_data in data.iteritems():
      # Store a list of properties
      for key in item_data:
        self.items_properties.add(key)

      item_id = int(item_id.lstrip("item_"))
      name = item_data.get("Name")
      desc = item_data.get("Description")
      skill_reqs = item_data.get("SkillReqs")
      required_appearance = item_data.get("RequiredAppreance")
      effects = item_data.get("EffectDescs", [])
      effects = [self._FormatEffect(e) for e in effects]
      slot = item_data.get("EquipSlot")
      value = int(item_data.get("Value"))
      icon_id = int(item_data.get("IconId"))
      keywords = item_data.get("Keywords")
      self.items[item_id] = Item(name=name, description=desc, id=item_id, required_appearance=required_appearance, skill_reqs=skill_reqs, value=value, icon=icon_id, effects=effects, slot=slot, keywords=keywords, version=self.version)

  def ParseEffects(self):
    data = self._OpenDataFile("effects.json")

    for item_id, item_data in data.iteritems():
      # Store a list of properties
      for key in item_data:
        self.effects_properties.add(key)
        
  def ParseTSysClientInfo(self):
    data = self._OpenDataFile("tsysclientinfo.json")

    max_effects_num = 0
    for power_id, power_data in data.iteritems():
      # Store a list of properties
      power_id = int(power_id.lstrip("power_"))
      suffix = power_data.get("Suffix")
      prefix = power_data.get("Prefix")
      _tiers = power_data.get("Tiers")
      tiers = dict()
        
      for tier, tier_data in _tiers.iteritems():
        tier_num = int(tier.lstrip("id_"))
        tier_effects = tier_data.get("EffectDescs")
        tiers[tier_num] = [self._FormatEffect(effect) for effect in tier_effects]
        max_effects_num = max(max_effects_num, len(tier_effects))

      for key in power_data:
        self.powers_properties.add(key)

      self.powers[power_id] = Power(prefix=prefix, suffix=suffix, tiers=tiers)
      for ability_name, skill_bonus, chance, flat_bonus, flat_chance, source in self.ExtractDamageMod(self.powers[power_id]):
        logging.info("Found mod %s(%s, %s, %s, %s) in %s", ability_name, skill_bonus, chance, flat_bonus, flat_chance, tiers[tier_num][0])
        if not skill_bonus and not flat_bonus:
          continue
        for _, ability in self.abilities.iteritems():
          if ability.name.startswith(ability_name):
            if skill_bonus:
              ability.mods["SkillBase"].append((skill_bonus, chance, source))
              ability.mods["SkillBase"].append((skill_bonus, chance, source))
            if flat_bonus:
              ability.mods["SkillFlat"].append((flat_bonus, flat_chance, source))
              if flat_chance < 1.0:
                ability.mods["SkillFlat"].append((flat_bonus, flat_chance, source))

  def FindAbilitiesInMod(self, mod):
    blacklist = ["XP", "Armor to", "For"]
    abilities = re.findall(("("  # Catch each skill name
                            "(?:[A-Z][A-Za-z_\\-\\']+)"  # Skill names start with Capitalized
                            "(?: (?:of|to|of the|['A-Z][A-Za-z_\\-\\']*))" # Continueswith "X of the X" or "X to Y" or "Say I Love You"
                            "*"  # Or maybe it has no 2nd component, like "Punch"
                            ")+"),  # But there can be more than one.
                            mod)
    # Handle combo mods
    if abilities and abilities[0] == "Combo":
      yield abilities[-1]
    else:
      for ability in abilities:
        if ability in blacklist:
          continue
        else:
          yield ability

  def FindBonusesInMod(self, mod):
    skill_bonus = chance = flat_bonus = flat_chance = None
    try:
      # Screech deals +15% damage
      # Scintillating Flame and Scintillating Frost deal +45% damage
      skill_bonus = re.search("deals? \+([0-9]+)% damage", mod).group(1)
      skill_bonus = int(skill_bonus) / 100.0
      chance = 1
    except AttributeError:
      pass

    try:
      # Fireball and Frostball have a 33% chance to deal +65% damage"
      # Fire Breath has a 50% chance to deal +3% damage and restore 2 Armor to you"
      skill_bonus, chance = re.search("([0-9]+)% chance to deal \+([0-9]+)% damage", mod).groups()
      skill_bonus = int(skill_bonus) / 100.0
      chance = int(chance) / 100.0
    except AttributeError:
      pass

    try:
      # King of the Forest has a 50% chance to deal +15 damage
      # Werewolf Bite attacks have a 50% chance to deal 12 extra damage
      flat_bonus, flat_chance = re.search("([0-9]+)% chance to deal \+([0-9]+) damage", mod).groups()
      flat_bonus = int(flat_bonus) / 100.0
      flat_chance = int(flat_chance) / 100.0
    except AttributeError:
      pass

    try:
      # Screech deals +15 damage
      flat_bonus = re.search("deals? \+([0-9]+) damage", mod).group(1)
      flat_bonus = int(flat_bonus)
      flat_chance = 1
    except AttributeError:
      pass

    return skill_bonus, chance, flat_bonus, flat_chance

  def ExtractDamageMod(self, power):
    last_tier = sorted(power.tiers.keys())[-1]
    last_tiers_effects = sorted(power.tiers[last_tier])
    for effect in last_tiers_effects:
      affected_abilities = self.FindAbilitiesInMod(effect)
      skill_mod, chance, flat_bonus, flat_chance = self.FindBonusesInMod(effect)
      for ability in affected_abilities:
        yield ability, skill_mod, chance, flat_bonus, flat_chance, power.prefix or power.suffix

  def ParseAttributes(self):
    data = self._OpenDataFile("attributes.json")

    for attribute, attr_data in data.iteritems():
      # Store a list of properties
      label = attr_data.get("Label")
      id_ = attr_data.get("Id")
      is_hidden = attr_data.get("IsHidden", False)
      self.attributes[attribute] = Attribute(id=id_, name=attribute, label=label, is_hidden=is_hidden)

      for key in attr_data:
        self.attr_properties.add(key)

  def ParseSkills(self):
    data = self._OpenDataFile("skills.json")
    rewards_properties = set()

    for skill, skill_data in data.iteritems():
      # Store a list of properties
      id_ = skill_data.get("Id")
      desc = skill_data.get("Description")
      combat = skill_data.get("Combat", False)
      maxlevel = skill_data.get("MaxLevel")
      advtable = skill_data.get("AdvancementTable")
      xptable = skill_data.get("XpTable")
      _rewards = skill_data.get("Rewards")
      name = skill_data.get("Name", skill)
      rewards = {}
      for level, reward_dict in _rewards.iteritems():
        level = int(level)
        grant_ability = reward_dict.get("Ability")
        if grant_ability:
          grant_ability = "Ability granted: %s" % self.abilities.get(grant_ability, grant_ability)
        skill_bonus = reward_dict.get("BonusToSkill")
        if skill_bonus:
          skill_bonus = "+1 %s" % self.skills.get(skill_bonus, skill_bonus)
        recipe_bonus = reward_dict.get("Recipe")
        note_bonus = reward_dict.get("Notes")
        rewards[level] = filter(None, [grant_ability, skill_bonus, recipe_bonus, note_bonus])

      self.skills[skill] = Skill(id=id_, name=name, description=desc, combat=combat, maxlevel=maxlevel, rewards=rewards, advtable=advtable, xptable=xptable)

      for key in skill_data:
        self.skills_properties.add(key)

  def _FindAbilityDamage(self, ability):
    damage = ability.get("PvE", {}).get("Damage")
    if damage:
      return int(damage)

    for effect in ability.get("PvE", {}).get("TargetEffects", []):
      if effect.startswith("NecroReap"):
        try:
          return int(re.match("NecroReap\(([0-9]+)\)", effect).group(1))
        except (IndexError, AttributeError):
          pass
    return damage

  def ParseAbilities(self):
    data = self._OpenDataFile("abilities.json")
    pve_properties = set()

    for ability, ability_data in data.iteritems():
      # Store a list of properties
      id_ = int(ability.lstrip("ability_"))
      desc = ability_data.get("Description")
      name = ability_data.get("Name", ability)
      damage = self._FindAbilityDamage(ability_data)
      damage_type = ability_data.get("DamageType")
      internal_name = ability_data.get("InternalName")

      power_cost = ability_data.get("PvE", {}).get("PowerCost")
      if power_cost:
        range_ = int(power_cost)

      range_ = ability_data.get("PvE", {}).get("Range")
      if range_:
        range_ = int(range_)

      cooldown = ability_data.get("ResetTime")
      if cooldown:
        cooldown = int(cooldown)

      level = ability_data.get("Level")
      if level:
        level = int(level)

      skill = ability_data.get("Skill")
      self.ability2skill[internal_name] = skill

      self.abilities[id_] = Ability(id=id_, name=name, description=desc, damage=damage, damage_type=damage_type, internal_name=internal_name, range=range_, power_cost=power_cost, cooldown=cooldown, level=level, skill=skill)
      #self.abilities[internal_name] = self.abilities[id_]
      for p in ability_data.get("PvE"):
        pve_properties.add(p)

    print pve_properties

  def _GetRecipeItem(self, item):
    item_code = item.get("ItemCode")
    item_keys = item.get("ItemKeys")
    desc = item.get("Desc")

    stack_size = item.get("StackSize")

    try:
      stack_size = int(stack_size)
    except ValueError:
      pass

    if not item_code:
      return desc, stack_size

    try:
      item_code = int(item_code)
      item = self.items.get(item_code, "ITEM_%s" % item_code)
    except ValueError:
      pass
    except TypeError:
      import ipdb;ipdb.set_trace()
      pass

    return item, stack_size

  def ParseRecipes(self):
    data = self._OpenDataFile("recipes.json")

    for recipe, recipe_data in data.iteritems():
      # Store a list of properties
      id_ = int(recipe.lstrip("recipe_"))
      name = recipe_data.get("Name")
      internal_name = recipe_data.get("InternalName")
      description = recipe_data.get("Description")
      ingredients_json = recipe_data.get("Ingredients", [])
      ingredients = []
      for item in ingredients_json:
        item, num = self._GetRecipeItem(item)
        ingredients.append((item, num))

      iconid = recipe_data.get("IconId")
      skill = recipe_data.get("Skill")
      skill = self.skills.get(skill) or skill
      skill_level_req = recipe_data.get("SkillLevelReq")
      try:
        skill_level_req = int(skill_level_req)
      except ValueError:
        pass

      results_json = recipe_data.get("ResultItems")
      results = []
      for item in results_json:
        item, num = self._GetRecipeItem(item)
        results.append((item, num))
      
      server_info = recipe_data.get("ServerInfo")
      reward_skill = server_info.get("RewardSkill")
      reward_skill_xp = server_info.get("RewardSkillXp")
      reward_skill_xp_1st = server_info.get("RewardSkillXpFirstTime")
      try:
        reward_skill_xp_1st = int(reward_skill_xp_1st)
      except ValueError:
        pass
        
      try:
        reward_skill_xp = int(reward_skill_xp)
      except ValueError:
        pass

      recipe_obj = Recipe(id=id_, name=name, desc=description, iconid=iconid, internal_name=internal_name, skill=skill, skill_level_req=skill_level_req, reward_skill=reward_skill, reward_skill_xp_1st=reward_skill_xp_1st, reward_skill_xp=reward_skill_xp, ingredients=ingredients, results=results)
      self.recipes[id_] = recipe_obj
      self.recipes[internal_name] = recipe_obj

      for key in recipe_data:
        self.recipe_properties.add(key)

    print self.recipe_properties


class BaseGorgonObject(object):
  def __init__(self, **kwargs):
    pass

  def __unicode__(self):
    return unicode(self.name) or repr(self)

  def __str__(self):
    return str(self.name) or repr(self)


class Item(BaseGorgonObject):
  def __init__(self, name=None, description=None, id=None, required_appearance=None, skill_reqs=None, value=None, effects=None, slot=None, icon=None, version=None, keywords=None, **kwargs):
    super(Item, self).__init__(**kwargs)
    self.version = version
    self.name = name
    self.description = description
    self.id = id
    self.required_appearance = required_appearance
    self.skill_reqs = skill_reqs
    self.value = value
    self.effects = effects or []
    self.slot = slot
    self.icon = icon
    self.keywords = keywords or []

  @property
  def icon_img(self):
    if self.icon:
      return u"<img src=\"http://cdn.projectgorgon.com/v%d/icons/icon_%s.png\">" % (self.version, self.icon)
    
  def __unicode__(self):
          return u"%s (%dc): '%s'" % (self.name, self.value, self.description)


class Recipe(BaseGorgonObject):
  def __init__(self, id=None, name=None, desc=None, iconid=None, internal_name=None, skill=None, skill_level_req=None, reward_skill=None, reward_skill_xp=None, reward_skill_xp_1st=None, ingredients=None, results=None, **kwargs):
    super(Recipe, self).__init__(**kwargs)
    self.id = id
    self.name = name
    self.desc = desc
    self.iconid = iconid
    self.internal_name = internal_name
    self.skill = skill
    self.skill_level_req = skill_level_req
    self.reward_skill = reward_skill
    self.reward_skill_xp = reward_skill_xp
    self.reward_skill_xp_1st = reward_skill_xp_1st
    self.ingredients = ingredients
    self.results = results


class Ability(BaseGorgonObject):
  def __init__(self, id=None, name=None, description=None, damage=None, damage_type=None, internal_name=None, range=None, power_cost=None, cooldown=None, skill=None, level=None, **kwargs):
    super(Ability, self).__init__(**kwargs)
    self.id = id
    self.name = name
    self.description = description
    self.damage = damage
    self.damage_type = damage_type
    self.internal_name = internal_name
    self.range = range
    self.power_cost = power_cost
    self.cooldown = cooldown
    self.skill = skill or "Unknown"
    self.level = level
    self.mods = dict(SkillBase=[], SkillFlat=[])


class Skill(BaseGorgonObject):
  def __init__(self,id=None, name=None, description=None, combat=False, maxlevel=None, rewards=None, advtable=None, xptable=None, **kwargs):
    super(Skill, self).__init__(**kwargs)
    self.id = id
    self.name = name
    self.description = description
    self.combat = combat
    self.maxlevel = maxlevel
    self.rewards = rewards or {}
    self.advtable = advtable
    self.xptable = xptable

  def __unicode__(self):
    return unicode(self.name)

  def __str__(self):
    return str(self.name)


class Attribute(BaseGorgonObject):
  def __init__(self, id=None, name=None, label=None, is_hidden=None, **kwargs):
    super(Attribute, self).__init__(**kwargs)
    self.id = id
    self.name = name
    self.label = label
    self.is_hidden = is_hidden or False

  def __unicode__(self):
    return self.label

  def __str__(self):
    return str(self.label)


class Power(BaseGorgonObject):
  def __init__(self, prefix=None, suffix=None, tiers=None, skill=None, **kwargs):
    super(Power, self).__init__(**kwargs)
    self.prefix = prefix
    self.suffix = suffix
    self.tiers = tiers
    self.skill = None


def html(func):
  def f(*args, **kwargs):
    header = """<html>
    <head>
      <link rel="stylesheet" type="text/css" href="//cdn.datatables.net/1.10.10/css/jquery.dataTables.css">
      <link rel="stylesheet" type="text/css" href="/style.css">
      <link rel="stylesheet" type="text/css" href="http://cdn.jsdelivr.net/qtip2/2.2.1/basic/jquery.qtip.min.css">
      <script type="text/javascript" charset="utf8" src="https://code.jquery.com/jquery-1.12.0.min.js"></script>
      <script type="text/javascript" charset="utf8" src="//cdn.datatables.net/1.10.10/js/jquery.dataTables.js"></script>
      <script type="text/javascript" charset="utf8" src="http://cdnjs.cloudflare.com/ajax/libs/qtip2/2.2.1/basic/jquery.qtip.min.js"></script>
    </head>
    <body>
      <script>
        $(document).ready(function() {
          $('table').DataTable({
            "info":   false
            })
          .on('mouseover', '.tooltip', function(event) {
              overwrite: false,
              $(this).qtip({
                  content: {
                        text: 'Loading...',
                        ajax: {
                            url: $(this).attr('rel')
                        } 
                  },
                  show: {
                      event: event.type,
                      ready: true,
                      solo: true
                  },
                  position: {viewport: $(window)}
              });
          });
        });
      </script>
      <div><a href="powers.html">MODS</a> | <a href="items.html">ITEMS</a> | <a href="skills.html">SKILLS</a> | <a href="abilities.html">ABILITIES</a> | <a href="recipes.html">RECIPES</a></div>
      """
    footer = """</body></html>"""

    return header + func(*args, **kwargs) + footer
  return f


class Reporter(object):
  def __init__(self, parser):
    self.parser = parser
    self.calculator = Calculator(parser)

  @html
  def ItemsReport(self):
    output = u'<table class="display" cellspacing="0" width="100%"><thead><tr><th>Icon</th><th>Type</th><th>Name</th><th>Description</th><th>Effects</th><th>Keywords</th></tr></thead><tbody>'
    for item in sorted(self.parser.items.values(), key=lambda x:x.slot):
      output += u"<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
        item.icon, item.slot, item.name, item.description, u'<br>'.join(item.effects), u'<br>'.join(item.keywords))
    output += u"</tbody></table></body></html>"
    return output

  @html
  def RecipesReport(self):
    output = u'<table class="display" cellspacing="0" width="100%"><thead><tr><th>Skill</th><th>Level</th><th>Name</th><th>Ingredients</th><th>Results</th><th>XP</th></tr></thead><tbody>'
    for recipe in sorted(self.parser.recipes.values(), key=lambda x:x.skill.name):
      output += u"<tr><td>%s</td><td>%s</td><td><a class=\"tooltip\" rel=\"items/item_%d.html\">%s</a></td><td>%s</td><td>%s</td><td>%s</td></tr>" % (
        recipe.skill, recipe.skill_level_req, recipe.id, recipe.name,
        u'<br>'.join([u'%d <a class=\"tooltip\" rel=\"items/item_%d.html\">%s</a>' % (i[1], getattr(i[0], "id", 0), getattr(i[0], "name", i[0])) for i in recipe.ingredients]),
        u'<br>'.join([u'%d <a class=\"tooltip\" rel=\"items/item_%d.html\">%s</a>' % (i[1], getattr(i[0], "id", 0), getattr(i[0], "name", i[0])) for i in recipe.results]),
        u'%d (%d)' % (recipe.reward_skill_xp, recipe.reward_skill_xp_1st))
    output += u"</tbody></table></body></html>"
    return output



  @html
  def PowersReport(self):
    output =  u'<table class="display" cellspacing="0" width="100%"><thead><tr><th>Skill</th><th>Prefix</th><th>Suffix</th><th>Effects</th></tr></thead><tbody>'
    for power in sorted(self.parser.powers.values(), key=lambda x:x.prefix):
      tier_effects = ""
      for tier_num, effects in power.tiers.iteritems():
        tier_effects += u"<tr><td>%d</td><td>%s</td>" % (tier_num, u'<br>'.join(effects))
      output += u"<tr><td>%s</td><td>%s</td><td>%s</td><td><table>%s</table></td></tr>" % (power.skill, power.prefix, power.suffix, tier_effects)
    output += u"</tbody></table>"
    return output

  @html
  def SkillsReport(self):
    output = ""
    for name, skill in sorted(self.parser.skills.iteritems(), key=lambda x:x[1].name):
      output += u'''<a href="#skill%d"><h1>%s</h1></a>
      <p>%s</p>
      <table class="display" cellspacing="0" width="100%%">
        <thead>
          <tr><th>Level</th><th>Reward</th><th>Description</th><th>Details</th></tr>
        </thead>
        <tbody''' % (skill.id, skill.name, skill.description)

      for level, rewards in sorted(skill.rewards.iteritems()):
        for reward in rewards:
          if isinstance(reward, Skill):
            output += u'<tr><td>%d</td><td>Skill: %s</td><td>%s</td><td>%s</td></tr>' % (level, reward.name, reward.description, u"")
          else:
            output += u'<tr><td>%d</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (level, reward, u'', u'')
      output += u"</tbody></table>"
    return output

  @html
  def AbilitiesReport(self):
    output = u'''
    <table class="display" cellspacing="0" width="100%%">
      <thead>
        <tr><th>Skill</th><th>Level</th><th>Name</th><th>Damage</th><th>Power</th><th>Cooldown</th><th>mDAM (mods)</th><th>aDAM (mods)</th><th>%%</th><th>aDAM DPS</th><th>MDAM (mods)</th><th>% mods</th><th>+dmg mods</th><th>Description</th></tr>
      </thead>
      <tbody'''

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

      adam_dps = ""
      if ability.cooldown > 0 and avg:
        adam_dps = "%.0f" % (int(avg) / float(ability.cooldown))
      output += u'<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % (
        ability.skill, ability.level, ability.name, ability.damage or '-', ability.power_cost or '-', ability.cooldown or '-', min_, avg, pct, adam_dps, max_, "+".join(percent_mods), "+".join(flat_mods), ability.description)
    output += u"</tbody></table>"
    return output

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
        keywords = u'<br>'.join(item.keywords)
        fd.write(u"""
<html>
  <head><title>{name}</title></head>
  <body>
    <div style="float: left">{iconimg}</div>
    <div class="stats">
    <p>{title}</p>
    <p>{desc}</p>
    <table>
      <tr><td>Value:</td><td>{value}</td><td>Slot:</td><td>{slot}</td></tr>
      <tr><td>Keywords:</td><td colspan="3">{keywords}</td></tr>
    <table>
  </body>
</html>""".format(name=item.name, iconimg=item.icon_img, title=item.name, desc=item.description, value=item.value, slot=item.slot, keywords=item.keywords))



class Calculator(object):
  def __init__(self, parser):
    self.parser = parser

  def CalculateMinDamage(self, ability_base_damage, base_ability_mod, ability_pct_mods, ability_flat_mods):
    if not ability_base_damage:
      return

    pct_mod = 1
    for pct, chance, _ in ability_pct_mods:
      if chance and chance < 1.0:
        continue
      pct_mod += pct

    flat_mod = 0
    for flat, chance, _ in ability_flat_mods:
      if chance and chance < 1.0:
        continue
      flat_mod += flat

    return ability_base_damage *(base_ability_mod+pct_mod) + flat_mod;

  def CalculateAvgDamage(self, ability_base_damage, base_ability_mod, ability_pct_mods, ability_flat_mods):
    if not ability_base_damage:
      return None, None

    damage = ability_base_damage * (1+base_ability_mod)
    avg_ability_mod = 0.0
    chance = 0.0
    chance_cnt = 0

    for base_mod, chance, _ in ability_pct_mods:
      avg_ability_mod += base_mod * chance
      damage += ability_base_damage * base_mod * chance
      if chance < 1.0:
        chance += chance
        chance_cnt += 1

    for flat, chance, _ in ability_flat_mods:
      damage += flat * chance * (1+avg_ability_mod)
      if chance < 1.0:
        chance += chance
        chance_cnt += 1

    if chance_cnt:
      return damage, chance / chance_cnt
    return damage, 1

  def CalculateMaxDamage(self, ability_base_damage, base_ability_mod, ability_pct_mods, ability_flat_mods):
    if not ability_base_damage:
      return

    damage = ability_base_damage * (1+base_ability_mod)
    skill_mods = 0

    for pct, _, _ in ability_pct_mods:
      damage += int(ability_base_damage * pct)
      skill_mods += pct

    for flat, _, _ in ability_flat_mods:
      damage += flat*(1+skill_mods)

    return damage

  def CalculateDamage(self, ability_id):
    ability = self.parser.abilities[ability_id]
    min = self.CalculateMinDamage(ability.damage, 0.8, ability.mods["SkillBase"], ability.mods["SkillFlat"])
    avg, pct = self.CalculateAvgDamage(ability.damage, 0.8, ability.mods["SkillBase"], ability.mods["SkillFlat"])
    max = self.CalculateMaxDamage(ability.damage, 0.8, ability.mods["SkillBase"], ability.mods["SkillFlat"])
    return min, avg, pct, max


if __name__ == "__main__":
  logging.basicConfig(level=logging.DEBUG)
  try:
    version = 248
    parser = GorgonJsonParser(version)
    reporter = Reporter(parser)

    import ipdb;ipdb.set_trace()
    BASE_PATH = "/var/www/html/v%d" % version
    try:
      os.makedirs(BASE_PATH)
    except OSError:
      pass

    codecs.open(os.path.join(BASE_PATH, "items.html"), "wb", encoding="utf-8").write(reporter.ItemsReport())
    reporter.DumpItems(os.path.join(BASE_PATH, "items/"))
    codecs.open(os.path.join(BASE_PATH, "powers.html"), "wb", encoding="utf-8").write(reporter.PowersReport())
    codecs.open(os.path.join(BASE_PATH, "skills.html"), "wb", encoding="utf-8").write(reporter.SkillsReport())
    codecs.open(os.path.join(BASE_PATH, "abilities.html"), "wb", encoding="utf-8").write(reporter.AbilitiesReport())
    codecs.open(os.path.join(BASE_PATH, "recipes.html"), "wb", encoding="utf-8").write(reporter.RecipesReport())
  except Exception:
    import pdb
    pdb.post_mortem(sys.exc_info()[2])
    raise
