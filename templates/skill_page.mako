<%!
    from gorgon.utils import myescape, itemlink, build_ingredient
    from itertools import chain
    from gorgon import model
%>


<a href="#skill${skill.id}"><h1>${skill.name}</h1></a>
<p>${skill.description}</p>
<script>
  $(document).ready(function() {
    $('#skill${skill.id}').DataTable({
      paging: false,
      info: false,
      data: dataSet${skill.id},
      columns: [
        { title: "Level" },
        { title: "Reward", className: "reward-name" },
        { title: "Description" },
      ],
    })
    .order([[0, "asc"]])
  });

  var dataSet${skill.id} = [

% for ability in filter(lambda x:x.skill == skill.internal_name, abilities):
%   if ability in list(chain.from_iterable(skill.rewards.values())):
    ["${ability.level}", "<span class=\"automatic\">ABILITY: ${ability.name | myescape}</span>", "${ability.description | myescape}"],
%   else:
    ["${ability.level}", "ABILITY: ${ability.name | myescape}", "${ability.description | myescape}"],
%   endif
% endfor
% for recipe in filter(lambda x:x.skill == skill, recipes):
%   if recipe in list(chain.from_iterable(skill.rewards.values())):
    ["${recipe.skill_level_req}", "<span class=\"automatic\">RECIPE: ${recipe.name | myescape}</span>", "${recipe.description | myescape}"],
%   else:
    ["${recipe.skill_level_req}", "RECIPE: ${recipe.name | myescape}", "${recipe.description | myescape}"],
%   endif
% endfor
% for level, rewards in skill.rewards.iteritems():
%   for reward in rewards:
%     if isinstance(reward, model.Skill):
    ["${level}", "<span class=\"automatic\">+1 ${reward.name| myescape}</span>", "${reward.description | myescape}"],
%     elif isinstance(reward, unicode):
    ["${level}", "<span class=\"automatic\">${reward| myescape}</span>", ""],
%     endif
%   endfor
% endfor
  ];
</script>
    <table id="skill${skill.id}" class="display compact table table-striped table-bordered skill-table" cellspacing="0" width="100%">
    </table>


% if skill.subskills:
<h1>Sub-skills</h1>
%   for subskill in sorted(skill.subskills, key=lambda x:x.name):
<a href="#skill${subskill.id}"><h2>${subskill.name}</h2></a>
<p>${subskill.description}</p>
<script>
  $(document).ready(function() {
    $('#skill${subskill.id}').DataTable({
      paging: false,
      info: false,
      data: dataSet${subskill.id},
      columns: [
        { title: "Level" },
        { title: "Reward", className: "reward-name" },
        { title: "Description" },
        { title: "Details" },
      ],
    })
    .order([[0, "asc"]])
  });

  var dataSet${subskill.id} = [

%   for ability in filter(lambda x:x.skill == subskill.internal_name, abilities):
%     if ability in list(chain.from_iterable(subskill.rewards.values())):
    ["${ability.level}", "<span class=\"automatic\">ABILITY: ${ability.name | myescape}</span>", "${ability.description | myescape}", ""],
%     else:
    ["${ability.level}", "${ability.name | myescape}", "${ability.description | myescape}", ""],
%     endif
%   endfor
%   for recipe in filter(lambda x:x.skill == subskill, recipes):
%     if recipe in list(chain.from_iterable(subskill.rewards.values())):
    ["${recipe.skill_level_req}", "<span class=\"automatic\">RECIPE: ${recipe.name | myescape}</span>", "${recipe.description | myescape}", ""],
%     else:
    ["${recipe.skill_level_req}", "RECIPE: ${recipe.name | myescape}", "${recipe.description | myescape}", ""],
%     endif
%   endfor

% for level, rewards in subskill.rewards.iteritems():
%   for reward in rewards:
%     if isinstance(reward, model.Skill):
    ["${level}", "<span class=\"automatic\">+1 ${reward.name| myescape}</span>", "${reward.description | myescape}", ""],
%     elif isinstance(reward, unicode):
    ["${level}", "<span class=\"automatic\">${reward| myescape}</span>", "", ""],
%     endif
%   endfor
% endfor
  ];
</script>
    <table id="skill${subskill.id}" class="display compact table table-striped table-bordered skill-table" cellspacing="0" width="100%">
    </table>
%   endfor
% endif