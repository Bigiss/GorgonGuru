<%!
    from gorgon.utils import myescape, itemlink, build_ingredient
%>


% for skill in sorted(skills, key=lambda x:x.name):
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

%   if skill.rewards:
%     for level, rewards in skill.rewards.iteritems():
%       for reward in rewards:
%         if getattr(reward, "name", None): 
    ["${level}", "${reward.name}", "${reward.description}", ""],
%         else:
    ["${level}", "${reward}", "", ""],
%         endif
%       endfor
%     endfor
  ];
</script>
    <table id="skill${skill.id}" class="display" cellspacing="0" width="100%">
    </table>

%   endif
% endfor
