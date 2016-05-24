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
];