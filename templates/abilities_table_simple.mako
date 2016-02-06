<%!
    from gorgon.utils import myescape, itemlink
%>

<script>
  $(document).ready(function() {
    $('#abilities').DataTable({
      data: dataSetAbilities,
      fixedHeader: {
          headerOffset: $('#navMenu').outerHeight()
      },
      paging: false,
      searching: false,
      info: false,
      columns: [
        { title: "Skill" },
        { title: "Level" },
        { title: "Name", contentPadding: "mmmmmmmmmm" },
        { title: "Damage" },
        { title: "Power" },
        { title: "Cooldown" },
        { title: "Description" },
      ]
    })
    .page.len(25)
    .order([[0, "asc"], [1, "asc"] ])
    .draw()
  });

  var dataSetAbilities = [

% for ability in abilities:
<%
    damage = ability.damage or "-"
    power = ability.power_cost or "-"
    cooldown = ability.cooldown or "-"
    icon_img = ability.RenderIcon(height=32, width=32)
%>
    ["${ability.skill | myescape}", ${ability.level | myescape}, "${icon_img|myescape} ${ability.name|myescape}", "${damage|myescape}", "${power|myescape}", "${cooldown|myescape}", "${ability.description|myescape}" ],
% endfor
  ];
</script>
    <table id="abilities" class="display table table-condensed table-striped table-bordered" cellspacing="0" width="100%">
    </table>