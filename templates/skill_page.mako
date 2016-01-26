<%!
    from gorgon.utils import myescape, itemlink, build_ingredient
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
        { title: "Reward" },
        { title: "Description" },
        { title: "Details" },
      ],
    })
  });

  var dataSet${skill.id} = [

% if skill.rewards:
%   for level, rewards in skill.rewards.iteritems():
%     for reward in rewards:
%       if getattr(reward, "name", None):
    ["${level}", "${reward.name | myescape}", "${reward.description | myescape}", ""],
%       else:
    ["${level}", "${reward | myescape}", "", ""],
%       endif
%     endfor
%   endfor
% endif
  ];
</script>
    <table id="skill${skill.id}" class="display compact table table-striped table-bordered" cellspacing="0" width="100%">
    </table>


% if skill.subskills:
<h1>Sub-skills</h1>
%   for subskill in sorted(skill.subskills, key=lambda x:x.name):
<a href="#skill${subskill.id}"><h2>${subskill.name}</h2></a>
<p>${subskill.description}</p>
%     if subskill.rewards:
<script>
  $(document).ready(function() {
    $('#skill${subskill.id}').DataTable({
      paging: false,
      info: false,
      data: dataSet${subskill.id},
      columns: [
        { title: "Level" },
        { title: "Reward" },
        { title: "Description" },
        { title: "Details" },
      ],
    })
  });

  var dataSet${subskill.id} = [

%       for level, rewards in subskill.rewards.iteritems():
%         for reward in rewards:
%           if getattr(reward, "name", None):
    ["${level}", "${reward.name | myescape}", "${reward.description | myescape}", ""],
%           else:
    ["${level}", "${reward | myescape}", "", ""],
%           endif
%         endfor
%       endfor
  ];
</script>
    <table id="skill${subskill.id}" class="display compact table table-striped table-bordered" cellspacing="0" width="100%">
    </table>
%     endif
%   endfor
% endif