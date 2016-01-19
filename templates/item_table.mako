<%!
    from gorgon.utils import myescape, itemlink
%>
<div class="page-header">
  <h1>Items</h1>
  <p class="lead">Use the items table to quickly find items of your interest.
  <ul>
    <li>Look for items that boost necromancy damage with a search for "necromancy damage +".</li>
    <li>Try finding the game <strong>admin</strong>'s items ;)</li>
  </ul>
</div>

<script>
  $(document).ready(function() {
    $('#items').DataTable({
      data: dataSet,
      dom: "<'row'<'col-sm-5'l><'col-sm-1'f><'col-sm-6'p>><'row'<'col-sm-12'tr>><'row'<'col-sm-5'i><'col-sm-7'p>>",
      fixedHeader: {
          headerOffset: $('#navMenu').outerHeight()
      },
      columns: [
        { title: "Slot" },
        { title: "Name" },
        { title: "Value" },
        { title: "Description" },
        { title: "Effects" },
        { title: "Keywords" }
      ]
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
    <table id="items" class="display compact table table-striped table-bordered" cellspacing="0" width="100%">
    </table>
