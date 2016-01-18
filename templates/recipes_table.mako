<%!
    from gorgon.utils import myescape, itemlink, build_ingredient
%>

<script>
  $(document).ready(function() {
    $('#recipes').DataTable({
      data: dataSet,
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
    })
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
    <table id="recipes" class="display" cellspacing="0" width="100%">
    </table>
