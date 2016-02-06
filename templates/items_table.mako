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
    $('#items').append('<tfoot></th><th class="filtercolumn" id="equipmentslot"></th><th class="filtercolumn" id="name"></th><th class="filtercolumn" id="value"></th><th class="filtercolumn" id="description"></th><th class="filtercolumn" id="effects"></th><th class="filtercolumn" id="keyword"></th></tr></tfoot>');
    $('#items').DataTable({
      data: dataSetItems,
      dom: "<'row'<'col-sm-3'l><'col-sm-3'f><'col-sm-6'p>><'row'<'col-sm-12'tr>><'row'<'col-sm-5'i><'col-sm-7'p>>",
      fixedHeader: {
          headerOffset: $('#navMenu').outerHeight()
      },
      columns: [
        { title: "Slot" },
        { title: "Name", "contentPadding": "mmmmmmmmmm" },
        { title: "Value" },
        { title: "Description" },
        { title: "Effects" },
        { title: "Keywords" }
      ],
      fnRowCallback: lazy_imageload
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

    // Setup - add a text input to each footer cell
    $('#items tfoot th.filtercolumn').each( function () {
        var that = this;
        var startingValue = "";
        window.location.hash.substr(1).split("&").forEach(function (el, idx, array) {
            var column = el.split(":")[0];
            var value = el.split(":")[1];
            if (that.id == column.toLowerCase()) {
                startingValue = value;
            }

        });
        var title = $(this).text();
        $(this).html( '<input type="text" placeholder="Search '+title+'" value="'+startingValue+'"/>' );

    } );

    // DataTable
    var table = $('#items').DataTable();

    // Apply the search
    table.columns().every( function () {
        var that = this;

        var input = $('input', this.footer())
        if (input.val()) {
            this.search(input.val()).draw();
        };
        $( 'input', this.footer() ).on( 'keyup change', function () {
            if ( that.search() !== this.value ) {
                that
                    .search( this.value )
                    .draw();
            }
        } );
    } );

} );

  var dataSetItems = [

% for item in items:
<%
    effects = u'\n'.join(item.effects or [])
    keywords = u'\n'.join(item.keywords or [])
    link = itemlink(item)
    icon_img = item.RenderIcon(hidden=True)
    slot = item.slot or ""
%>
    ["${slot}", "${icon_img|myescape} ${link | myescape}", ${item.value}, "${item.description | myescape}", "${effects | myescape}", "${keywords | myescape}" ],
% endfor
  ];
</script>
    <table id="items" class="display table table-condensed table-striped table-bordered" cellspacing="0" width="100%">
    </table>