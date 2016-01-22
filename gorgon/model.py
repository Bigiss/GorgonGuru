from mako.template import Template


class IconMixin(object):
    """A mixin to be able to render icons."""

    def RenderIcon(self):
        if self.icon:
            template = Template(u"<img src=\"http://cdn.projectgorgon.com/v${version}/icons/icon_${iconid}.png\">")
            return template.render(version=self.version, iconid=self.icon or "unknown")


class BaseGorgonObject(object):
    """Base class for all Gorgon objects."""

    def __init__(self, **kwargs):
        pass

    def __unicode__(self):
        return unicode(self.name) or repr(self)

    def __str__(self):
        return str(self.name) or repr(self)


class Item(BaseGorgonObject, IconMixin):
    """Base class for all Gorgon items."""

    def __init__(self, name=None, description=None, id=None, required_appearance=None, skill_reqs=None, value=None,
                 effects=None, slot=None, icon=None, version=None, keywords=None, stack_size=None, **kwargs):
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
        self.stack_size = stack_size or 1

    def __unicode__(self):
        return u"%s (%dc): '%s'" % (self.name, self.value, self.description)


class Recipe(BaseGorgonObject, IconMixin):
    def __init__(self, id=None, name=None, desc=None, iconid=None, internal_name=None, skill=None, skill_level_req=None,
                 reward_skill=None, reward_skill_xp=None, reward_skill_xp_1st=None, ingredients=None, results=None,
                 **kwargs):
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
    def __init__(self, id=None, name=None, description=None, damage=None, damage_type=None, internal_name=None,
                 range=None, power_cost=None, cooldown=None, skill=None, level=None, **kwargs):
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
    def __init__(self, id=None, name=None, description=None, combat=False, maxlevel=None, rewards=None, advtable=None,
                 xptable=None, parents=None, **kwargs):
        super(Skill, self).__init__(**kwargs)
        self.id = id
        self.name = name
        self.description = description
        self.combat = combat or False
        self.maxlevel = maxlevel
        self.rewards = rewards or {}
        self.advtable = advtable
        self.xptable = xptable
        self.parents = parents or []

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
