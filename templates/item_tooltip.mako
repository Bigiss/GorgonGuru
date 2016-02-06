<%
  from gorgon.utils import colorize

  effects = colorize(u"<br>".join(item.effects or []))
  iconimg = item.RenderIcon()
  slot = item.slot or "-"
%>
<html>
  <head>
    <title>${item.name}</title>
    <link rel="stylesheet" type="text/css" href="/style.css">
  </head>
  <body>
    <div class="itemdescription">
      <div class="header">
        <div class="icon">${iconimg}</div>
        <div class="title">${item.name}</div>
        <div class="desc">${item.description}</div>
      </div>
      <div class="main">
        <div class="effects">
          ${effects}
        </div>
      </div>
      <div class="footer">
        <div class="value">Value: ${item.value}</div>
        <div class="stack">Stack: ${item.stack_size}</div>
% if item.keywords:
        <div id="keywords">
            <ul>
%   for keyword in item.keywords:
                <li>${keyword}</li>
%   endfor
            </ul>
        </div>
% endif
% if item.sellers:
        <div id="sellers">
            Sold by: <ul>
%   for seller in item.sellers:
%      if seller.Item(item).multiple > 1:
                <li>${seller.name} (${seller.Item(item).multiple} for ${seller.Item(item).price})</li>
%      else:
                <li>${seller.name} (${seller.Item(item).price})</li>
%      endif:
%   endfor
            </ul>
        </div>
% endif
      </div>
    </div>
  </body>
</html>
