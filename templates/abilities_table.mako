<%!
    from gorgon.utils import myescape, itemlink
%>
<div class="page-header">
  <h1>Abilities</h1>
  <p class="lead">A table with all available (and some unobtainable) abilities in the data files.</p>
  <p>The table includes experimental columns to calculate potential damage of each skill accounting for mods.
  <ul>
    <li><strong>mDAM</strong> is the minimum damage the ability would do if you had all the damage mods for it. It assumes all chance-based mods didn't trigger.</li>
    <li><strong>aDAM</strong> is the average damage the ability will in the long run. It averages chance-based mods and should be more representative.</li>
    <li><strong>MDAM</strong> is the maximum damage the ability will ever do on a single cast. Assuming all mods trigger.</li>
  </ul>
  <p>There's many variables that affect damage that are not taken into account yet. For example: +damage mods from gear, element vulnerabilities and resistances, critical hits, critical damage mods, etc. For now, it's only meant to provide some guidance. Please report <a href="https://github.com/dmnthia/gorgon/issues">any bugs in github</a></p>
  <div class="alert alert-warning"><strong>BE WARNED:</strong> Columns with <span class="label label-danger">BETA</span> are inaccurate.</div>
</div>

<script>
  $(document).ready(function() {
    $('#abilities').DataTable({
      data: dataSet,
      fixedHeader: {
          headerOffset: $('#navMenu').outerHeight()
      },
      dom: "<'row'<'col-sm-5'l><'col-sm-1'f><'col-sm-6'p>><'row'<'col-sm-12'tr>><'row'<'col-sm-5'i><'col-sm-7'p>>",
      columns: [
        { title: "Skill" },
        { title: "Level" },
        { title: "Name" },
        { title: "Damage" },
        { title: "Power" },
        { title: "Cooldown" },
        { title: "mDAM <span class=\"label label-danger\">BETA</span>" },
        { title: "aDAM <span class=\"label label-danger\">BETA</span>" },
        { title: "%% <span class=\"label label-danger\">BETA</span>" },
        { title: "aDAM DPS <span class=\"label label-danger\">BETA</span>" },
        { title: "MDAM<span class=\"label label-danger\">BETA</span>" },
        { title: "% mods <span class=\"label label-danger\">BETA</span>" },
        { title: "+flat mods <span class=\"label label-danger\">BETA</span>" },
        { title: "Description" },
      ]
    })
    .page.len(25)
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
    <table id="abilities" class="display compact table table-striped table-bordered" cellspacing="0" width="100%">
    </table>

