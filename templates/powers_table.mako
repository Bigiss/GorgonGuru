<%!
    from gorgon.utils import myescape, itemlink, build_ingredient
%>
<div class="page-header">
  <h1>Mods</h1>
  <p class="lead">Use the following table to list all mods for a particlar skill.</p>
  <ul>
    <li>Type "See Red" in the search box to find all mods for this skill</li>
  </ul>
</div>

<script>
  $(document).ready(function() {
    $('#mods').DataTable({
      data: dataSet,
      dom: "<'row'<'col-sm-5'l><'col-sm-1'f><'col-sm-6'p>><'row'<'col-sm-12'tr>><'row'<'col-sm-5'i><'col-sm-7'p>>",
      fixedHeader: {
          headerOffset: $('#navMenu').outerHeight()
      },
      columns: [
        { title: "Skill" },
        { title: "Prefix" },
        { title: "Suffix" },
        { title: "Effects" },
      ],
    })
    .page.len(25)
    .order([[0, "asc"]])
    .draw()
    .on('mouseover', '.tooltip', function(event) {
        overwrite: false,
        $(this).qtip({
            content: {
                  text: 'Loading...',
                  ajax: {
                      url: $(this).attr('rel')
                  } 
            },
            show: {
                event: event.type,
                ready: true,
                solo: true
            },
            position: {viewport: $(window)}
        });
    })
  });

  var dataSet = [

% for power in powers:
<%
    tiers = u"<br>".join([u"TIER %d: %s" % (t[0], u"<br>".join(t[1])) for t in power.tiers.iteritems()])
%>
    ["${power.skill | myescape}", "${power.prefix | myescape}", "${power.suffix | myescape}", "${tiers | myescape}"],
% endfor
  ];
</script>

    <table id="mods" class="display compact table table-striped table-bordered" cellspacing="0" width="100%">
    </table>
