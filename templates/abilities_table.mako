<%!
    from gorgon.utils import myescape, itemlink
%>
<script>
  $(document).ready(function() {
    $('#abilities').DataTable({
      data: dataSet,
      columns: [
        { title: "Skill" },
        { title: "Level" },
        { title: "Name" },
        { title: "Damage" },
        { title: "Power" },
        { title: "Cooldown" },
        { title: "mDAM (mods)" },
        { title: "aDAM (mods)" },
        { title: "%%" },
        { title: "aDAM DPS" },
        { title: "MDAM (mods)" },
        { title: "% mods" },
        { title: "+flat mods" },
        { title: "Description" },
      ]
    })
    .order([[0, "asc"], [1, "asc"] ])
    .draw()
  });

  var dataSet = [

% for ability_ in abilities:
<%
    ability, mDAM, aDAM, aDAMpct, MDAM, pct_mods, flat_mods = ability_
    damage = ability.damage or "-"
    power = ability.power_cost or "-"
    cooldown = ability.cooldown or "-"
    aDAMdps = ""
    if ability.cooldown > 0 and aDAM:
      aDAMdps = "%.0f" % (int(aDAM) / float(ability.cooldown))
    pct_mods = u"+".join(pct_mods)
    flat_mods = u"+".join(flat_mods)
%>
    ["${ability.skill | myescape}", ${ability.level | myescape}, "${ability.name|myescape}", "${damage|myescape}", "${power|myescape}", "${cooldown|myescape}", "${mDAM}", "${aDAM}", "${aDAMpct}", "${aDAMdps}", "${MDAM}", "${pct_mods|myescape}", "${flat_mods|myescape}", "${ability.description|myescape}" ],
% endfor
  ];
</script>
    <table id="abilities" class="display" cellspacing="0" width="100%">
    </table>

