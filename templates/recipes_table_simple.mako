<%!
    from gorgon.utils import myescape, itemlink, build_ingredient
    from gorgon import model
%>
<script>
  // Generate the table
  $(document).ready(function() {
    $('#recipes').DataTable({
      data: dataSetRecipes,
      fixedHeader: {
          headerOffset: $('#navMenu').outerHeight()
      },
      paging: false,
      searching: false,
      info: false,
      columns: [
        { title: "Skill" },
        { title: "Level" },
        { title: "Name" },
        { title: "Ingredients" },
        { title: "Results" },
        { title: "Value" },
        { title: "XP" }
      ],
    })
    .page.len(25)
    .order([[0, "asc"], [1, "asc"], [2, "asc"]])
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
              classes: "qtip-tipsy"
            }
        });
    });

  });

  var dataSetRecipes = [

% for recipe in recipes:
<%
    ingredients = u"\n".join([build_ingredient(ingredient, with_image=True) for ingredient in recipe.ingredients])
    results = [build_ingredient(result, with_image=True) for result in recipe.results]

    result_effects = []
    for result, description in recipe.result_effects:
        if isinstance(result, model.Item):
            result_effects.append(u"%s %s %s" % (result.RenderIcon(),
                                                 itemlink(result),
                                                 description))
        else:
            result_effects.append(description)
    results = "\n".join(results + result_effects)

    result_value = sum([int(result[0])*int(result[1].value) for result in recipe.results if isinstance(result[1], model.Item)])
%>
    ["${recipe.skill | myescape}", "${recipe.skill_level_req | myescape}", "${recipe.name | myescape}", "${ingredients | myescape}", "${results | myescape}", ${result_value}, "${recipe.reward_skill_xp} (${recipe.reward_skill_xp_1st})"],
% endfor
  ];
</script>
    <table id="recipes" class="display table table-compact table-condensed table-striped table-bordered">
    </table>
