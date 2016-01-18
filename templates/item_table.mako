<%!
    from gorgon.utils import myescape, itemlink
%>
<script>
  $(document).ready(function() {
    $('#items').DataTable({
      data: dataSet,
      columns: [
        { title: "Slot" },
        { title: "Name" },
        { title: "Value" },
        { title: "Description" },
        { title: "Effects" },
        { title: "Keywords" }
      ]
    })
    .order([[0, "asc"], [1, "asc"] ])
    .draw()
    .on('mouseover', '.item', function(event) {
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
            position: {viewport: $(window)},
            style: {
                classes: 'qtip-tipsy'
            }
        });
    })

  });

  var dataSet = [

% for item in items:
<%
    effects = u'\n'.join(item.effects)
    keywords = u'\n'.join(item.keywords)
    link = itemlink(item)
    icon_img = item.RenderIcon()
    slot = item.slot or ""
%>
    ["${slot}", "${link | myescape}", ${item.value}, "${item.description | myescape}", "${effects | myescape}", "${keywords | myescape}" ],
% endfor
  ];
</script>
    <table id="items" class="display" cellspacing="0" width="100%">
    </table>
