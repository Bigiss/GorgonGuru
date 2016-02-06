
<div class="page-header">
  <h1>Abilities</h1>
  <p class="lead">A table with all available (and some unobtainable) abilities in the data files.</p>
  <p>The table includes experimental columns to calculate potential damage of each skill accounting for mods.
  <ul>
    <li><strong>mDMG</strong> is the minimum damage the ability would do if you had all the damage mods for it. It assumes all chance-based mods didn't trigger.</li>
    <li><strong>aDMG</strong> is the average damage the ability will in the long run. It averages chance-based mods and should be more representative.</li>
    <li><strong>MDMG</strong> is the maximum damage the ability will ever do on a single cast. Assuming all mods trigger.</li>
  </ul>
  <p>There's many variables that affect damage that are not taken into account yet. For example: +damage mods from gear, element vulnerabilities and resistances, critical hits, critical damage mods, etc. For now, it's only meant to provide some guidance. Please report <a href="https://github.com/dmnthia/gorgon/issues">any bugs in github</a></p>
  <div class="alert alert-warning"><strong>BE WARNED:</strong> Columns with <span class="label label-danger">BETA</span> are inaccurate.</div>
</div>

<%include file="abilities_table.mako"/>
