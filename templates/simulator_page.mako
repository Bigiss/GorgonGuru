    <div class="page-header">
        <h1>Build simulator <span class="label label-danger">ALPHA</span></h1>
        <p>Start by choosing your skill combo and then apply all mods. When you're done, share your amazing build by copying and sharing the address bar in your browser. </p>
    </div>
    <h2>Equipment & Mods</h2>
    <div class="builder">
        <div class="skill">
            Pick your skill combination: <select id="firstskill" onchange="Simulator.onSetFirstSkill($(this));"></select> <select id="secondskill" onchange="Simulator.onSetSecondSkill($(this));"></select>
        </div>
        <div class="slots">

% for slot in ["Head", "Necklace", "Chest", "Hands", "Ring", "MainHand", "OffHand", "Legs", "Feet"]:
%  if not (loop.index % 2):
            <div class="row ">
%  endif
                <div class="slot ${slot} col-md-3">
                    <div class="itemdescription">
                        <div class="header">
                            <div class="icon"></div>
                            <div class="title normal">${slot}</div>
                            <div class="desc">Placeholder ${slot} slot.</div>
                        </div>
                        <div class="main">
                            <div id="${slot}"></div>
                        </div>
                        <div class="footer">
                            <div class="value">Value: $$$</div>
                        </div>
                    </div>
                </div>
                <div class="col-md-3">
                    <p>Select the mods below.</p>
                    <select id="${slot}-1" onchange="Simulator.onSetSlotMod('${slot}', 1, $(this));"></select>
                    <select id="${slot}-2" onchange="Simulator.onSetSlotMod('${slot}', 2, $(this));"></select>
                    <select id="${slot}-3" onchange="Simulator.onSetSlotMod('${slot}', 3, $(this));"></select>
                    <select id="${slot}-4" onchange="Simulator.onSetSlotMod('${slot}', 4, $(this));"></select>
                    <select id="${slot}-5" onchange="Simulator.onSetSlotMod('${slot}', 5, $(this));"></select>
                    <select id="${slot}-6" onchange="Simulator.onSetSlotMod('${slot}', 6, $(this));"></select>
                </div>
%  if loop.index % 2:
            </div>
%  endif
%endfor
        </div>
    </div>
    <script src="generated_powers.js"></script>
    <script src="builder.js"></script>
    <script>
        var Simulator = new GorgonBuildSimulator();
        Simulator.Initialize(mods);
    </script>