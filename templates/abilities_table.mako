<%!
    from gorgon.utils import myescape, itemlink
%>

<script>
  $(document).ready(function() {
    function lazy_imageload(nRow, aData, iDisplayIndex)
    {
        var img = $('img.loading', nRow);
        img.attr('src', img.attr('orig'));
        return nRow;
    };
    $('#abilities').DataTable({
      data: dataSet,
      fixedHeader: {
          headerOffset: $('#navMenu').outerHeight()
      },
      dom: "<'row'<'col-sm-5'l><'col-sm-1'f><'col-sm-6'p>><'row'<'col-sm-12'tr>><'row'<'col-sm-5'i><'col-sm-7'p>>",
      columns: [
        { title: "Skill" },
        { title: "LV" },
        { title: "Name" },
        { title: "DMG" },
        { title: "POW" },
        { title: "CD" },
        { title: "mDMG <span class=\"label label-danger\">BETA</span>" },
        { title: "aDMG <span class=\"label label-danger\">BETA</span>" },
        { title: "%% <span class=\"label label-danger\">BETA</span>" },
        { title: "aDPS <span class=\"label label-danger\">BETA</span>" },
        { title: "MDMG <span class=\"label label-danger\">BETA</span>" },
        { title: "% mods <span class=\"label label-danger\">BETA</span>" },
        { title: "+flat mods <span class=\"label label-danger\">BETA</span>" },
        { title: "DESC", contentPadding: "mmmmmmmmmmmmmmmmmmmmmmmmmmmm" },
      ],
      fnRowCallback: lazy_imageload
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
    cooldown = str(ability.cooldown) or "-"
    aDAMdps = ""
    if ability.cooldown > 0 and aDAM:
      cd = ability.cooldown
      # Adjust for global cooldown
      if cd == 1:
        cooldown += "*"
        cd = 1.3
      aDAMdps = "%.0f" % (int(aDAM) / float(cd))
    pct_mods = u"+".join(pct_mods)
    flat_mods = u"+".join(flat_mods)
    icon_img = ability.RenderIcon(hidden=True, height=32, width=32)
%>
    ["${ability.skill | myescape}", ${ability.level | myescape}, "${icon_img|myescape} ${ability.name|myescape}", "${damage|myescape}", "${power|myescape}", "${cooldown|myescape}", "${mDAM}", "${aDAM}", "${aDAMpct}", "${aDAMdps}", "${MDAM}", "${pct_mods|myescape}", "${flat_mods|myescape}", "${ability.description|myescape}" ],
% endfor
  ];
</script>
    <table id="abilities" class="display table table-condensed table-striped table-bordered" cellspacing="0" width="100%">
    </table>
