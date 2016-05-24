import codecs
import json
import logging
import os
import re

from gorgon import model


class GorgonJsonParser(object):
    CRAFTING_SKILLS = [
        "Alchemy",
        "Artistry",
        "Blacksmithing",
        "BuckleArtistry",
        "Carpentry",
        "Cheesemaking",
        "Cooking",
        "DyeMaking",
        "Fletching",
        "Leatherworking",
        "Mycology",
        "Tailoring",
        "Tanning",
        "Textiles",
        "Toolcrafting"]

    FORAGING_SKILLS = [
        "Butchering",
        "Fishing",
        "Foraging",
        "Geology",
        "Mining",
        "Surveying"]

    def __init__(self, version=None):
        self.version = version
        self.attributes = dict()
        self.attr_properties = set()
        self.attributes_alias = dict()
        self.items_properties = set()
        self.items = dict()
        self.items_alias = dict()
        # Stores a list of all unique ItemKeys so they can be exported for recipe popups.
        self.item_keys = set()
        self.effects = dict()
        self.effects_properties = set()
        self.effects_alias = dict()
        self.abilities = dict()
        self.abilities_properties = set()
        self.abilities_alias = dict()
        self.ability2skill = dict()
        self.skills = dict()
        self.skills_properties = set()
        self.skills_alias = dict()
        self.powers = dict()
        self.powers_properties = set()
        self.powers_alias = dict()
        self.recipes = dict()
        self.recipe_properties = set()
        self.recipes_alias = dict()
        self.merchants = dict()
        self.merchants_alias = dict()
        self.data_directory = None

    def Parse(self, directory):
        """Initializes this parser by parsing source JSON files."""
        self.data_directory = directory
        self.version_directory = os.path.join(directory, "v%d" % self.version)
        self.ParseAttributes()
        self.ParseItems()
        self.ParseEffects()
        self.ParseAbilities()
        self.ParseRecipes()
        self.ParseSkills()
        self.PostprocessSkills()
        self.ParseTSysClientInfo()
        self.ParseMerchants()
        self.LinkRecipesToSkills()

    def _OpenDataFile(self, filename):
        """Helper function to load JSON data files."""
        file_path = os.path.join(self.version_directory, filename)
        data = {}
        try:
            data = json.load(codecs.open(file_path, "rb", encoding="latin-1"))
        except (IOError, TypeError):
            pass
        return self.Overlay(data, filename)

    def Overlay(self, json_dict, filename):
        """Applies the relevant overlay to the data source file."""
        overlay_path = os.path.join(self.data_directory, *["overlays", filename])
        try:
            overlay = json.load(codecs.open(overlay_path, "rb", encoding="latin-1"))
        except (IOError, TypeError):
            return json_dict
        json_dict.update(overlay)
        return json_dict

    def _ParseEffect(self, effect):
        """Obtains all parameters for effects."""
        regexp = ("{(?P<attr>[^}]+)}"
                  "{(?P<value>[^}]+)}"
                  "{?(?P<restr>[^}]+)?}?")
        matches = re.match(regexp, effect)
        if not matches:
            # This is a standard description
            return effect, None, None

        return matches.group("attr"), matches.group("value"), matches.group("restr")

    def _FormatEffect(self, effect):
        """Formats effects in a human_readable way."""
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
            internal_name = item_data.get("InternalName")
            required_appearance = item_data.get("RequiredAppreance")
            effects = item_data.get("EffectDescs", [])
            effects = [self._FormatEffect(e) for e in effects]
            slot = item_data.get("EquipSlot")
            value = int(item_data.get("Value", 0))
            stack_size = int(item_data.get("MaxStackSize", 1))
            icon_id = int(item_data.get("IconId"))
            keywords = item_data.get("Keywords")
            item = model.Item(name=name, description=desc, id=item_id,
                              required_appearance=required_appearance, skill_reqs=skill_reqs,
                              value=value, icon=icon_id, effects=effects, slot=slot, keywords=keywords,
                              version=self.version, stack_size=stack_size, internal_name=internal_name)
            self.items[item_id] = item
            self.items_alias[item_id] = item
            self.items_alias[name] = item
            self.items_alias[internal_name] = item

    def GetItem(self, id_, default=None):
        return self.items_alias.get(id_, default)

    def ParseEffects(self):
        data = self._OpenDataFile("effects.json")

        for effect_id, data in data.iteritems():
            # Store a list of properties

            effect_id = int(effect_id.lstrip("effect_"))
            name = data.get("Name")
            desc = data.get("Desc")
            icon = data.get("IconId")
            duration = data.get("Duration")

            for key in data:
                self.effects_properties.add(key)

            effect = model.Effect(id=effect_id, name=name, desc=desc, icon=icon, duration=duration)
            self.effects[effect_id] = effect
            self.effects_alias[effect_id] = effect
            self.effects_alias[name] = effect

    def ParseTSysClientInfo(self):
        data = self._OpenDataFile("tsysclientinfo.json")

        max_effects_num = 0
        for power_id, power_data in data.iteritems():
            # Store a list of properties
            power_id = int(power_id.lstrip("power_"))
            suffix = power_data.get("Suffix")
            prefix = power_data.get("Prefix")
            _tiers = power_data.get("Tiers")
            slots = power_data.get("Slots")
            skill = power_data.get("Skill")
            tiers = dict()

            for tier, tier_data in sorted(_tiers.iteritems()):
                tier_num = int(tier.lstrip("id_"))
                tier_effects = tier_data.get("EffectDescs")
                tiers[tier_num] = [self._FormatEffect(effect) for effect in tier_effects]
                max_effects_num = max(max_effects_num, len(tier_effects))

            for key in power_data:
                self.powers_properties.add(key)

            power = model.Power(prefix=prefix, suffix=suffix, tiers=tiers, slots=slots, skill=skill)
            self.powers[power_id] = power
            self.powers_alias[power_id] = power


            for ability_name, skill_bonus, chance, flat_bonus, flat_chance, source in self.ExtractDamageMod(
                    self.powers[power_id]):
                logging.debug("Found mod %s(%s, %s, %s, %s) in %s", ability_name, skill_bonus, chance, flat_bonus,
                             flat_chance, tiers[max(tiers.keys())][0])
                if not skill_bonus and not flat_bonus:
                    continue
                for _, ability in self.abilities.iteritems():
                    if ability.name.startswith(ability_name):
                        slots = getattr(self.GetPower(power_id, {}), "slots", ["Dummy Slot"])
                        if slots:
                            num_slots = len(slots)
                        else:
                            num_slots = 2
                        for _ in range(num_slots):
                            if skill_bonus:
                                ability.mods["SkillBase"].append((skill_bonus, chance, source))
                            if flat_bonus:
                                ability.mods["SkillFlat"].append((flat_bonus, flat_chance, source))

    def GetPower(self, id_, default=None):
        return self.powers_alias.get(id_, default)

    def FindAbilitiesInMod(self, mod):
        blacklist = ["XP", "Armor to", "For"]
        abilities = re.findall(("("  # Catch each skill name
                                "(?:[A-Z][A-Za-z_\\-\\']+)"  # Skill names start with Capitalized
                                "(?: (?:of|to|of the|['A-Z][A-Za-z_\\-\\']*))"  # Continue with "X of the X" or "X to Y" or "Say I Love You"
                                "*"  # It may have no 2nd component, like "Punch"
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
            skill_bonus = re.search("deals? \+([0-9]+)%(?: health(?: and armor)?)? damage", mod).group(1)
            skill_bonus = int(skill_bonus) / 100.0
            chance = 1
        except AttributeError:
            pass

        try:
            # Fireball and Frostball have a 33% chance to deal +65% damage"
            # Fire Breath has a 50% chance to deal +3% damage and restore 2 Armor to you"
            chance, skill_bonus = re.search(
                    "([0-9]+)% chance to deal \+([0-9]+)%(?: health(?: and(?: \+[0-9]+%)? armor)?)? damage",
                    mod).groups()
            skill_bonus = int(skill_bonus) / 100.0
            chance = int(chance) / 100.0
        except AttributeError:
            pass

        try:
            # Screech deals +15 damage
            flat_bonus = re.search("deals? \+([0-9]+)(?: direct health)? damage", mod).group(1)
            flat_bonus = int(flat_bonus)
            flat_chance = 1
        except AttributeError:
            pass

        try:
            # King of the Forest has a 50% chance to deal +15 damage
            # Werewolf Bite attacks have a 50% chance to deal 12 extra damage
            flat_chance, flat_bonus = re.search("([0-9]+)% chance to deal \+([0-9]+)(?:(?: direct)? health)? damage",
                                                mod).groups()
            flat_bonus = int(flat_bonus)
            flat_chance = int(flat_chance) / 100.0
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
            attr_obj = model.Attribute(id=id_, name=attribute, label=label, is_hidden=is_hidden)
            self.attributes_alias[attribute] = attr_obj
            self.attributes_alias[attribute] = attr_obj
            self.attributes[attribute] = attr_obj
            for key in attr_data:
                self.attr_properties.add(key)

    def GetAttribute(self, id_, default=None):
        return self.attributes_alias.get(id_, default)

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
            parents = skill_data.get("Parents", [])
            _rewards = skill_data.get("Rewards")
            name = skill_data.get("Name", skill)
            crafting = skill in self.CRAFTING_SKILLS
            foraging = skill in self.FORAGING_SKILLS

            skill_obj = model.Skill(id=id_, name=name, description=desc, combat=combat, maxlevel=maxlevel,
                                _rewards=_rewards, advtable=advtable, xptable=xptable, parents=parents,
                                crafting=crafting, foraging=foraging, internal_name=skill)
            self.skills[id_] = skill_obj
            self.skills_alias[id_] = skill_obj
            self.skills_alias[name] = skill_obj
            self.skills_alias[skill] = skill_obj

            for key in skill_data:
                self.skills_properties.add(key)

    def PostprocessSkills(self):
        for skill in self.skills.values():
            if skill.parents:
                for parent in skill.parents:
                    parent_skill = self.GetSkill(parent)
                    if not parent_skill:
                        logging.error("Unable to find parent skill %s of %s", parent, skill.name)
                        continue
                    parent_skill.subskills.append(skill)
            rewards = {}
            for level, reward_dict in skill._rewards.iteritems():
                level = int(level)
                grant_ability = reward_dict.get("Ability")
                grant_ability = self.GetAbility(grant_ability, grant_ability)
                skill_bonus = reward_dict.get("BonusToSkill")
                skill_bonus = self.GetSkill(skill_bonus, skill_bonus)
                recipe_bonus = reward_dict.get("Recipe")
                recipe_bonus = self.GetRecipe(recipe_bonus, recipe_bonus)
                note_bonus = reward_dict.get("Notes")
                rewards[level] = filter(None, [grant_ability, skill_bonus, recipe_bonus, note_bonus])
            skill.rewards = rewards

    def GetSkill(self, id_, default=None):
        return self.skills_alias.get(id_, default)

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
            icon = ability_data.get("IconID")

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
            self.ability2skill[name] = skill
            self.ability2skill[ability] = skill
            ability_obj = model.Ability(id=id_, name=name, description=desc, damage=damage,
                                        damage_type=damage_type, internal_name=internal_name, range=range_,
                                        power_cost=power_cost, cooldown=cooldown, level=level, skill=skill, icon=icon,
                                        version=self.version)
            self.abilities[id_] = ability_obj
            self.abilities_alias[id_] = ability_obj
            self.abilities_alias[internal_name] = ability_obj
            self.abilities_alias[name] = ability_obj

            for p in ability_data.get("PvE"):
                pve_properties.add(p)

    def GetAbility(self, id_, default=None):
        return self.abilities_alias.get(id_, default)

    def _GetRecipeItem(self, item):
        item_code = item.get("ItemCode")
        item_keys = item.get("ItemKeys")
        desc = item.get("Desc")

        stack_size = item.get("StackSize")

        try:
            stack_size = int(stack_size)
        except ValueError:
            pass

        if item_code:
            try:
                item_code = int(item_code)
                item = self.GetItem(item_code, "ITEM_%s" % item_code)
            except ValueError:
                pass
            except TypeError:
                import ipdb;
                ipdb.set_trace()
                pass
            return item, stack_size
        elif item_keys:
            for key in item_keys:
                try:
                    _, _ = key.split(":")
                except ValueError:
                    key = "Keyword:" + key
                self.item_keys.add(key)
            return model.ItemFilter(keys=item_keys, desc=desc), stack_size
        else:
           return desc, stack_size


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
                ingredients.append((num, item))

            iconid = recipe_data.get("IconId")
            skill = recipe_data.get("Skill")
            skill = self.GetSkill(skill, skill)
            skill_level_req = recipe_data.get("SkillLevelReq")
            try:
                skill_level_req = int(skill_level_req)
            except ValueError:
                pass

            results_json = recipe_data.get("ResultItems")
            results = []
            for item in results_json:
                item, num = self._GetRecipeItem(item)
                results.append((num, item))

            result_effects_json = recipe_data.get("ResultEffects", [])
            result_effects = []
            for effect in result_effects_json:
                effect, description = self._ParseResultEffect(effect=effect)
                result_effects.append((effect, description))

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

            recipe_obj = model.Recipe(id=id_, name=name, description=description, icon=iconid, internal_name=internal_name,
                                      skill=skill, skill_level_req=skill_level_req, reward_skill=reward_skill,
                                      reward_skill_xp_1st=reward_skill_xp_1st, reward_skill_xp=reward_skill_xp,
                                      ingredients=ingredients, results=results, version=self.version,
                                      result_effects=result_effects)
            self.recipes[id_] = recipe_obj
            self.recipes_alias[id_] = recipe_obj
            self.recipes_alias[internal_name] = recipe_obj

            for key in recipe_data:
                self.recipe_properties.add(key)

    def GetRecipe(self, id_, default=None):
        return self.recipes_alias.get(id_, default)

    def _ParseResultEffect(self, effect):
        """Parses a recipe ResultEffects.

        Returns a tuple (result, description).
        """
        regexp = ("(?P<effect>[^(]+)"
                  "(?:\()(?P<params>[^)]+)(?:\))")
        matches = re.match(regexp, effect)
        if not matches:
            # This is a standard description
            return effect, effect

        parsed_effect = matches.group("effect")
        try:
            parsed_params = matches.group("params")
        except IndexError:
            parsed_params = None

        if parsed_effect == "TSysCraftedEquipment":
            item, maxenchanted, restriction = self._ParseCraftedEquipmentEffect(parsed_params)
            description = []
            if maxenchanted:
                description.append("(Max-Enchanted)")
            if restriction:
                description.append("(Restriction: %s)" % restriction)
            return item, u" ".join(description)
        else:
            return effect, effect

    def _ParseCraftedEquipmentEffect(self, params):
        params = params.split(",")
        if len(params) == 1:
            item = self.GetItem(params[0])
            return item, False, None
        elif len(params) == 2:
            item = self.GetItem(params[0])
            maxenchanted = int(params[1])
            return item, maxenchanted, None
        elif len(params) == 3:
            item = self.GetItem(params[0])
            maxenchanted = int(params[1])
            restriction = params[2]
            return item, maxenchanted, restriction
        else:
            import ipdb;ipdb.set_trace()


    def LinkRecipesToSkills(self):
        for recipe in self.recipes.values():
            recipe.skill = self.GetSkill(recipe.skill, recipe.skill)

    def GetRecipe(self, id_, default=None):
        return self.recipes_alias.get(id_, default)

    def ParseMerchants(self):
        merchants = self._OpenDataFile("merchants.json")
        for merchant_id, merchant in merchants.iteritems():
            merchant_obj = model.Merchant(name=merchant_id)
            sells = merchant.get("Sells", {})
            sales = {}
            for item_name, item_data in sells.iteritems():
                item_obj = self.GetItem(item_name)
                price = item_data.get("Price")
                if price:
                    price = int(price)
                multiple = item_data.get("Num")
                if multiple:
                    multiple = int(multiple)

                if not item_obj:
                    logging.error("Merchant %s sells unknown item %s", merchant_id, item_name)
                    continue
                sales[item_obj] = model.ShopItem(price=price, multiple=multiple)
                item_obj.sellers.append(merchant_obj)
            merchant_obj.sales = sales
            self.merchants[merchant_id] = merchant_obj
            self.merchants_alias[merchant_id] = merchant_obj


    def __sub__(self, other):
        new_items = dict([(id_, self.GetItem(id_)) for id_ in self.items if id_ not in other.items])
        new_powers = dict([(id_, self.GetPower(id_)) for id_ in self.powers if id_ not in other.powers])
        new_abilities = dict([(id_, self.GetAbility(id_)) for id_ in self.abilities if id_ not in other.abilities])
        new_recipes = dict([(id_, self.GetRecipe(id_)) for id_ in self.recipes if id_ not in other.recipes])
        new_skills = dict([(id_, self.GetSkill(id_)) for id_ in self.skills if id_ not in other.skills])
        additions = GorgonJsonParser()
        additions.items = new_items
        additions.powers = new_powers
        additions.abilities = new_abilities
        additions.recipes = new_recipes
        additions.skills = new_skills

        changes = {
            "items": {},
            "abilities": {},
            "powers": {},
            "recipes": {},
        }

        for item_id, item in self.items.iteritems():
            other_item = other.GetItem(item_id)
            if not other_item:
                continue
            diffs = item.Differences(other_item)
            if diffs:
                changes["items"][item] = diffs

        for ability_id, ability in self.abilities.iteritems():
            other_ability = other.GetAbility(ability_id)
            if not other_ability:
                continue
            diffs = ability.Differences(other_ability)
            if diffs:
                changes["abilities"][ability] = diffs

        for power_id, power in self.powers.iteritems():
            other_power = other.GetPower(power_id)
            if not other_power:
                continue
            diffs = power.Differences(other_power)
            if diffs:
                changes["powers"][power] = diffs

        for recipe_id, recipe in self.recipes.iteritems():
            other_recipe = other.GetRecipe(recipe_id)
            if not other_recipe:
                continue
            diffs = recipe.Differences(other_recipe)
            if diffs:
                changes["recipes"][recipe] = diffs

        return additions, changes
