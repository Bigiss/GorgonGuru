class Calculator(object):
    """A damage calculator for skills."""

    def __init__(self, parser):
        self.parser = parser

    def CalculateMinDamage(self, ability_base_damage, base_ability_mod, ability_pct_mods, ability_flat_mods):
        if not ability_base_damage:
            return

        pct_mod = 0
        for pct, chance, _ in ability_pct_mods:
            if chance < 1.0:
                continue
            pct_mod += pct

        flat_mod = 0
        for flat, chance, _ in ability_flat_mods:
            if chance < 1.0:
                continue
            flat_mod += flat

        return ability_base_damage * (1+ base_ability_mod + pct_mod) + flat_mod*(1+pct_mod)

    def CalculateAvgDamage(self, ability_base_damage, base_ability_mod, ability_pct_mods, ability_flat_mods):
        if not ability_base_damage:
            return None, None

        avg_ability_mod = 0
        avg_flat_mod = 0
        avg_chance = 0
        n = 0

        for base_mod, chance, _ in ability_pct_mods:
            avg_ability_mod += base_mod * chance
            if chance < 1.0:
                avg_chance += chance
                n += 1

        for flat, chance, _ in ability_flat_mods:
            avg_flat_mod += flat * chance
            if chance < 1.0:
                avg_chance += chance
                n += 1

        if n == 0:
            avg_chance = 1
            n = 1

        damage = ability_base_damage * (1+base_ability_mod+avg_ability_mod) + avg_flat_mod * (1+avg_ability_mod)
        return damage, (avg_chance/n)

    def CalculateMaxDamage(self, ability_base_damage, base_ability_mod, ability_pct_mods, ability_flat_mods):
        if not ability_base_damage:
            return

        ability_mod = 0
        flat_mod = 0

        for pct, _, _ in ability_pct_mods:
            ability_mod += pct

        for flat, _, _ in ability_flat_mods:
            flat_mod += flat

        return ability_base_damage * (1+ability_mod+base_ability_mod) + flat_mod*(1+ability_mod)

    def CalculateDamage(self, ability_id):
        ability = self.parser.GetAbility(ability_id)
        if not ability:
            raise ValueError("Ability with id %s not found" % ability_id)
        min_ = self.CalculateMinDamage(ability.damage, 0.8, ability.mods["SkillBase"], ability.mods["SkillFlat"])
        avg, pct = self.CalculateAvgDamage(ability.damage, 0.8, ability.mods["SkillBase"], ability.mods["SkillFlat"])
        max_ = self.CalculateMaxDamage(ability.damage, 0.8, ability.mods["SkillBase"], ability.mods["SkillFlat"])
        return min_, avg, pct, max_
