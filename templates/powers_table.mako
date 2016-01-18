<%!
    from gorgon.utils import myescape, itemlink, build_ingredient
%>

<script>
  $(document).ready(function() {
    $('#mods').DataTable({
      data: dataSet,
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

    <table id="mods" class="display" cellspacing="0" width="100%">
    </table>
