<%!
    from gorgon.utils import myescape, itemlink, build_ingredient
%>
var mods = [
% if powers:
    % for power_id, power in powers.iteritems():
<%
    slots = [myescape(slot).encode("utf-8") for slot in power.slots]
    description = power.tiers[power.tiers.keys()[-1]][0]
%>  [${power_id}, "${power.skill | myescape}", "${power.prefix | myescape}", "${power.suffix | myescape}", ${slots}, "${description}", "", 0, 0, 0, 0],
    % endfor
% endif
<<<<<<< HEAD
];
=======
];
>>>>>>> 6f8d1a610d6d91b4717933358f9221dfb329e353
