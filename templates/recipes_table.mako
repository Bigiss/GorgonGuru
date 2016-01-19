<%!
    from gorgon.utils import myescape, itemlink, build_ingredient
%>
<div class="page-header">
  <h1>Recipes</h1>
  <p class="lead">Use the recipes table to quickly find recipes of your interest. The search box on your right is your friend:
  <ul>
    <li>Type "Blacksmithing" on the search box to find all recipes of the Blacksmithing class or that contain the word</li>
    <li>Type "Red Apple" to find all recipes you could craft with that <span class="itemtooltip" rel="items/item_5309.html">Red Apple</span> you just picked</li>
  </ul>
</div>
<script>
  // Generate the table
  $(document).ready(function() {
    $('#recipes').DataTable({
      data: dataSet,
      dom: "<'row'<'col-sm-5'l><'col-sm-1'f><'col-sm-6'p>><'row'<'col-sm-12'tr>><'row'<'col-sm-5'i><'col-sm-7'p>>",
      fixedHeader: {
          headerOffset: $('#navMenu').outerHeight()
      },
      columns: [
        { title: "Skill" },
        { title: "Level" },
        { title: "Name" },
        { title: "Ingredients" },
        { title: "Results" },
        { title: "XP" }
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
            show: {
                event: event.type,
                ready: true,
                solo: true
            },
            position: {viewport: $(window)},
            style: {
              classes: "qtip-tipsy"
            }
        });
    });

  });


  var dataSet = [

% for recipe in recipes:
<%
    ingredients = u"\n".join([build_ingredient(ingredient) for ingredient in recipe.ingredients])
    results = u"\n".join([build_ingredient(result) for result in recipe.results])
%>
    ["${recipe.skill | myescape}", "${recipe.skill_level_req | myescape}", "${recipe.name | myescape}", "${ingredients | myescape}", "${results | myescape}", "${recipe.reward_skill_xp} (${recipe.reward_skill_xp_1st})"],
% endfor
  ];
</script>
    <table id="recipes" class="display compact table table-striped table-bordered" cellspacing="0" width="100%">
    </table>
