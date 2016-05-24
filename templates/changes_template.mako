<h1>Update ${new_version}</h1>
  <p class="lead">What follows are the changes visible in the data files for update ${new_version}.</p>
    <div class="alert alert-warning"><strong>THIS SECTION IS IN BETA!</strong> Not all changes are detected yet.</div>
<h2>Additions</h2>

% if skills:
<h3>New skills</h3>
  <table class="compact table table-striped table-bordered">
    <thead>
      <tr><td>SKILL</td><td>Description</td>
    </thead>
    <tbody>
%   for skill in skills:
      <tr><td><a href="/skills/${skill.id}.html">${skill.name}</a></td><td>${skill.description}</td></tr>
%   endfor
    </tbody>
  </table>
% endif
% if abilities:
<h3>New abilities</h3>
<%include file="abilities_table_simple.mako"/>
% endif

% if powers:
<h3>New powers</h3>
<%include file="powers_table_simple.mako"/>
% endif

% if items:
<h3>New items</h3>
<%include file="items_table_simple.mako"/>
% endif

% if recipes:
<h3>New recipes</h3>
<%include file="recipes_table_simple.mako"/>
% endif

<h2>Changes</h2>

<div class="changes">
% if changes["items"]:
<h3>Item changes</h3>
    <div class="row">
    <div class="col-md-2"></div>
    <div class="col-md-6">
        <table class="changes display compact table table-striped table-bordered">
            <thead>
                <tr>
                    <td>Item</td>
                    <td>Attribute</td>
                    <td>Before</td>
                    <td></td>
                    <td>After</td>
                </tr>
            </thead>
            <tbody>
%   for item, item_changes in changes["items"].iteritems():
%     for attr, (before, after) in item_changes.iteritems():
<%
        if attr == "icon":
            before = '<img src="http://cdn.projectgorgon.com/v%d/icons/icon_%d.png" />' % (old_version, before)
            after = '<img src="http://cdn.projectgorgon.com/v%d/icons/icon_%d.png" />' % (new_version, after)
        if isinstance(before, list):
            before = "<br/>".join([str(b) for b in before])
        if isinstance(after, list):
            after = "<br/>".join([str(a) for a in after])
%>
                <tr><td class="ability-name">${item.name}</td><td class="attribute-name">${attr}</td><td>${before}</td><td class="arrows">&#x21c9;</td><td>${after}</td></tr>
%     endfor
%   endfor
            </tbody>
        </table>
    </div>
    <div class="col-md-2"></div>
</div>
% endif

% if changes["abilities"]:
<h3>Ability changes</h3>
    <div class="row">
    <div class="col-md-2"></div>
    <div class="col-md-6">
        <table class="changes display compact table table-striped table-bordered">
            <thead>
                <tr>
                    <td>Ability</td>
                    <td>Attribute</td>
                    <td>Before</td>
                    <td></td>
                    <td>After</td>
                </tr>
            </thead>
            <tbody>
%   for ability, ability_changes in sorted(changes["abilities"].iteritems(), key=lambda x:(x[0].skill,x[0].name)):
%     for attr, (before, after) in ability_changes.iteritems():
<%
        if isinstance(before, list):
            before = "<br/>".join([str(b) for b in before])
        if isinstance(after, list):
            after = "<br/>".join([str(a) for a in after])
%>
                <tr><td class="ability-name">${ability.name}</td><td class="attribute-name">${attr}</td><td>${before}</td><td class="arrows">&#x2192;</td><td>${after}</td></tr>
%     endfor
%   endfor
            </tbody>
        </table>
    </div>
    <div class="col-md-2"></div>
</div>
% endif

% if changes["powers"]:
<h3 id="modchanges">Mod changes</h3>
    <div class="row">
    <div class="col-md-1"></div>
    <div class="col-md-10">
        <table class="changes display compact table table-striped table-bordered">
            <thead>
                <tr>
                    <td>Mod skill</td>
                    <td>Attribute</td>
                    <td>Before</td>
                    <td></td>
                    <td>After</td>
                </tr>
            </thead>
            <tbody>
%   for mod, mod_changes in sorted(changes["powers"].iteritems(), key=lambda x:(x[0].prefix,x[0].suffix)):
%     for attr, (before, after) in mod_changes.iteritems():
<%
        # Skip not having slot data in 248
        if attr == "slots" and before == None or attr == "skill" and before == None:
            continue

        if isinstance(before, list):
            before = "<br/>".join([str(b) for b in before])
        elif isinstance(before, dict):
            before = "<br/>".join(["%s: %s" % (k, " ".join(v)) for (k, v) in before.iteritems()])

        if isinstance(after, list):
            after = "<br/>".join([str(a) for a in after])
        elif isinstance(after, dict):
            after = "<br/>".join(["%s: %s" % (k, " ".join(v)) for (k, v) in after.iteritems()])

%>
                <tr><td class="ability-name">${mod.skill}</td><td class="attribute-name">${attr}</td><td>${before}</td><td class="arrows">&#x2192;</td><td>${after}</td></tr>
%     endfor
%   endfor
            </tbody>
        </table>
    </div>
    <div class="col-md-1"></div>
</div>
% endif

% if changes["recipes"]:
<h3>Recipes changes</h3>
    <div class="row">
    <div class="col-md-2"></div>
    <div class="col-md-6">
        <table class="changes display compact table table-striped table-bordered">
            <thead>
                <tr>
                    <td>Recipe</td>
                    <td>Attribute</td>
                    <td>Before</td>
                    <td></td>
                    <td>After</td>
                </tr>
            </thead>
            <tbody>
%   for recipe, recipe_changes in sorted(changes["recipes"].iteritems(), key=lambda x:(x[0].skill,x[0].name)):
%     for attr, (before, after) in recipe_changes.iteritems():
<%
        if isinstance(before, list):
            before = "<br/>".join([str(b) for b in before])
        if isinstance(after, list):
            after = "<br/>".join([str(a) for a in after])
%>
                <tr><td class="recipe-name">${recipe.name}</td><td class="attribute-name">${attr}</td><td>${before}</td><td class="arrows">&#x2192;</td><td>${after}</td></tr>
%     endfor
%   endfor
            </tbody>
        </table>
    </div>
    <div class="col-md-2"></div>
</div>
% endif
</div>
