<%!
    from gorgon.utils import myescape, itemlink
%>

<script>
$(document).ready(function() {
    $('#items').DataTable({
      data: dataSetItems,
      fixedHeader: {
          headerOffset: $('#navMenu').outerHeight()
      },
      paging: false,
      searching: false,
      info: false,
      columns: [
        { title: "Slot" },
        { title: "Name", "contentPadding": "mmmmmmmmmm" },
        { title: "Value" },
        { title: "Description" },
        { title: "Effects" },
        { title: "Keywords" }
      ],
    })
    .page.len(25)
    .order([[0, "asc"], [1, "asc"] ])
    .draw()
    .on('mouseover', '.itemtooltip', function(event) {
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
            position: {viewport: $(window)},
            style: {
                classes: 'qtip-tipsy'
            }
        });
    });
} );

  var dataSetItems = [

% for item in items:
<%
    effects = u'\n'.join(item.effects or [])
    keywords = u'\n'.join(item.keywords or [])
    link = itemlink(item)
    icon_img = item.RenderIcon()
    slot = item.slot or ""
%>
    ["${slot}", "${icon_img|myescape} ${link | myescape}", ${item.value}, "${item.description | myescape}", "${effects | myescape}", "${keywords | myescape}" ],
% endfor
  ];
</script>
    <table id="items" class="display table table-condensed table-striped table-bordered" cellspacing="0" width="100%">
    </table>