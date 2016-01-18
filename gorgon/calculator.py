from mako.template import Template


class Calculator(object):
  """A damage calculator for skills."""

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

    return ability_base_damage *(base_ability_mod+pct_mod) + flat_mod

  def CalculateAvgDamage(self, ability_base_damage, base_ability_mod, ability_pct_mods, ability_flat_mods):
    if not ability_base_damage:
      return None, None

    avg_ability_mod = 1.0
    avg_flat_mod = 1.0
    avg_chance = 0.0
    avg_chance_num = 0

    for base_mod, chance, _ in ability_pct_mods:
      avg_ability_mod += base_mod * chance
      avg_chance += chance
      avg_chance_num += 1

    for flat, chance, _ in ability_flat_mods:
      avg_flat_mod = flat * chance
      avg_chance += chance
      avg_chance_num += 1

    chance = 1
    if avg_chance_num:
      chance = avg_chance / avg_chance_num

    damage = ability_base_damage*(base_ability_mod+avg_ability_mod)+(avg_flat_mod*avg_ability_mod)
    return damage, chance

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
    min_ = self.CalculateMinDamage(ability.damage, 0.8, ability.mods["SkillBase"], ability.mods["SkillFlat"])
    avg, pct = self.CalculateAvgDamage(ability.damage, 0.8, ability.mods["SkillBase"], ability.mods["SkillFlat"])
    max_ = self.CalculateMaxDamage(ability.damage, 0.8, ability.mods["SkillBase"], ability.mods["SkillFlat"])
    return min_, avg, pct, max_
