<%!
    from gorgon.utils import myescape, itemlink
%>
<html>
  <head>
    <link rel="stylesheet" type="text/css" href="/style.css">
  </head>
  <body>
    <div id="matching-items">
      <ul>
% for item in items[:10]:
<%
    link = itemlink(item)
    icon_img = item.RenderIcon()
%>
        <li>${icon_img} ${link}</li>
% endfor
% if len(items) > 10:
        <li>And more...</li>
% endif
      </ul>
    </div>
  </body>
</html>
