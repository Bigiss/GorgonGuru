<%!
    from gorgon.utils import myescape, itemlink, build_ingredient
%>
<script>
  $(document).ready(function() {
    $('#mods').DataTable({
      data: dataSetPowers,
      fixedHeader: {
          headerOffset: $('#navMenu').outerHeight()
      },
      paging: false,
      searching: false,
      info: false,
      columns: [
        { title: "Skill" },
        { title: "Prefix" },
        { title: "Suffix" },
        { title: "Slots" },
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
            hide: {
                fixed: true,
                delay: 400
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

  var dataSetPowers = [

% if powers:
%   for power in powers:
<%
      if power.tiers:
        tiers = u"<br>".join([u"TIER %d: %s" % (t[0], u"<br>".join(t[1])) for t in power.tiers.iteritems()])
      else:
        tiers = ""

      if power.slots:
        slots = u"<br/>".join([slot for slot in power.slots])
      else:
        slots = ""
%>
    ["${power.skill | myescape}", "${power.prefix | myescape}", "${power.suffix | myescape}", "${slots | myescape}", "${tiers | myescape}"],
%   endfor
% endif
  ];
</script>

    <table id="mods" class="display table table-condensed table-striped table-bordered" cellspacing="0" width="100%">
    </table>
