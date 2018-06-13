var hidden, state, visibilityChange;
"undefined" !== typeof document.hidden ? (hidden = "hidden",
visibilityChange = "visibilitychange",
state = "visibilityState") : "undefined" !== typeof document.mozHidden ? (hidden = "mozHidden",
visibilityChange = "mozvisibilitychange",
state = "mozVisibilityState") : "undefined" !== typeof document.msHidden ? (hidden = "msHidden",
visibilityChange = "msvisibilitychange",
state = "msVisibilityState") : "undefined" !== typeof document.webkitHidden && (hidden = "webkitHidden",
visibilityChange = "webkitvisibilitychange",
state = "webkitVisibilityState");
var _isNeedReload = !1
  , _isGraphLoaded = !1;
document.addEventListener(visibilityChange, function() {
    "visible" == document[state] ? _isNeedReload && ($("#MainCy").html(""),
    $("#TrTxt").removeClass("active"),
    getData(_currentKeyNo)) : _isGraphLoaded || (_isNeedReload = !0)
}, !1);
var cy, id, activeNode, _rootData, _rootNode, _COLOR = {
    node: {
        person: "#FD485E",
        company: "#4ea2f0",
        current: "#ff9e00"
    },
    border: {
        person: "#FD485E",
        company: "#128BED",
        current: "#EF941B"
    },
    line: {
        invest: "#fd485e",
        employ: "#4ea2f0",
        legal: "#4ea2f0"
    }
}, _currentKeyNo, _companyRadius = 35, _personRadius = 15, _circleMargin = 10, _circleBorder = 3, _layoutNode = {}, _isFocus = !1, _maxChildrenLength = 0;
function uniqeByKeys(c, b) {
    for (var a = [], d = {}, e = 0, g = c.length; e < g; e++) {
        var f;
        f = c[e];
        for (var h = b, k = h.length, l = []; k--; )
            l.push(f[h[k]]);
        f = l.join("|");
        f in d || (d[f] = !0,
        a.push(c[e]))
    }
    return a
}
Array.prototype.unique = function() {
    for (var c = [], b = {}, a = 0; a < this.length; a++)
        b[this[a]] || (c.push(this[a]),
        b[this[a]] = 1);
    return c
}
;
function cloneObj(c) {
    var b = {};
    c instanceof Array && (b = []);
    for (var a in c) {
        var d = c[a];
        b[a] = "object" === typeof d ? cloneObj(d) : d
    }
    return b
}
function getRootData(c) {
    for (var b = {
        nodes: [],
        links: []
    }, a = 0; a < c.length; a++)
        for (var d = c[a].graph.nodes, e = 0; e < d.length; e++) {
            var g = d[e]
              , f = {};
            f.nodeId = g.id;
            f.data = {};
            f.data.obj = g;
            f.data.showStatus = null;
            f.layout = {};
            f.layout.level = null;
            f.layout.singleLinkChildren = [];
            b.nodes.push(f);
            _currentKeyNo == f.data.obj.properties.keyNo && (_rootNode = f)
        }
    b.nodes = uniqeByKeys(b.nodes, ["nodeId"]);
    for (a = 0; a < c.length; a++)
        for (d = c[a].graph.relationships,
        e = 0; e < d.length; e++)
            g = d[e],
            f = {
                data: {}
            },
            f.data.obj = g,
            f.data.showStatus = null,
            f.sourceNode = getGraphNode(g.startNode, b.nodes),
            f.targetNode = getGraphNode(g.endNode, b.nodes),
            f.linkId = g.id,
            f.source = getNodesIndex(g.startNode, b.nodes),
            f.target = getNodesIndex(g.endNode, b.nodes),
            b.links.push(f);
    b.links = uniqeByKeys(b.links, ["linkId"]);
    setLevel(b.nodes, b.links);
    setCategoryColor(b.nodes, b.links);
    return b
}
function emplyRevert(c) {
    c.forEach(function(b, a) {
        if ("EMPLOY" == b.data.obj.type) {
            a = b.source;
            var d = b.sourceNode;
            b.source = b.target;
            b.sourceNode = b.targetNode;
            b.target = a;
            b.targetNode = d
        }
    })
}
function mergeLinks(c) {
    c.forEach(function(b, a) {
        "Person" == b.sourceNode.data.obj.labels[0] && "LEGAL" == b.data.obj.type && c.forEach(function(a, e) {
            b.linkId != a.linkId && b.sourceNode.nodeId == a.sourceNode.nodeId && b.targetNode.nodeId == a.targetNode.nodeId && "EMPLOY" == a.data.obj.type && c.splice(e, 1)
        });
        "Person" == b.sourceNode.data.obj.labels[0] && "EMPLOY" == b.data.obj.type && c.forEach(function(a, e) {
            b.linkId != a.linkId && b.sourceNode.nodeId == a.sourceNode.nodeId && b.targetNode.nodeId == a.targetNode.nodeId && "LEGAL" == a.data.obj.type && c.splice(e, 1)
        })
    })
}
function setLevel(c, b) {
    function a(a, b, d) {
        for (var c = [], e = 0; e < b.length; e++) {
            var f = b[e];
            a != f.sourceNode.nodeId || f.targetNode.layout.level ? a != f.targetNode.nodeId || f.sourceNode.layout.level || (f.sourceNode.layout.level = d,
            c.push(f.sourceNode)) : (f.targetNode.layout.level = d,
            c.push(f.targetNode))
        }
        return c = uniqeByKeys(c, ["nodeId"])
    }
    c = 1;
    var d = [];
    for (d.push(_rootNode); d.length; ) {
        for (var e = [], g = 0; g < d.length; g++) {
            var f = d[g];
            f.layout.level = c;
            e = e.concat(a(f.nodeId, b, c))
        }
        c++;
        d = e
    }
}
function setCategoryColor(c, b) {
    for (var a = 0; a < b.length; a++)
        b[a].sameLink = {
            length: 0,
            currentIndex: 0,
            isSetedSameLink: !1
        };
    for (a = 0; a < b.length; a++) {
        var d = b[a];
        if (0 == d.sameLink.isSetedSameLink) {
            d.sameLink.isSetedSameLink = !0;
            var e = d.sourceNode.nodeId
              , g = d.targetNode.nodeId
              , f = [];
            f.push(d);
            for (var h = 0; h < b.length; h++) {
                var k = b[h];
                d.linkId != k.linkId && !k.sameLink.isSetedSameLink && (k.sourceNode.nodeId == e && k.targetNode.nodeId == g || k.sourceNode.nodeId == g && k.targetNode.nodeId == e) && (f.push(k),
                k.sameLink.isSetedSameLink = !0)
            }
            for (d = 0; d < f.length; d++)
                e = f[d],
                e.sameLink.length = f.length,
                e.sameLink.currentIndex = d
        }
    }
    for (a = 0; a < c.length; a++)
        b = c[a],
        _currentKeyNo == b.data.obj.properties.keyNo ? (b.data.color = _COLOR.node.current,
        b.data.strokeColor = _COLOR.border.current) : "Company" == b.data.obj.labels[0] ? (b.data.color = _COLOR.node.company,
        b.data.strokeColor = _COLOR.border.company) : (b.data.color = _COLOR.node.person,
        b.data.strokeColor = _COLOR.border.person)
}
function setSingleLinkNodes(c) {
    function b(a, b) {
        for (var c = 0, d = !0, f = 0; f < b.length; f++) {
            var h = b[f];
            h.targetNode.nodeId != a && h.sourceNode.nodeId != a || c++;
            if (1 < c) {
                d = !1;
                break
            }
        }
        return d
    }
    c.forEach(function(a, d) {
        b(a.sourceNode.nodeId, c) && a.targetNode.layout.singleLinkChildren.push(a.sourceNode);
        b(a.targetNode.nodeId, c) && a.sourceNode.layout.singleLinkChildren.push(a.targetNode)
    })
}
function getNodesIndex(c, b) {
    for (var a = 0, d = 0; d < b.length; d++)
        if (c == b[d].nodeId) {
            a = d;
            break
        }
    return a
}
function isNodeExist(c, b) {
    for (var a = !1, d = 0; d < b.length; d++)
        if (c == b[d].nodeId) {
            a = !0;
            break
        }
    return a
}
function filterLinksByNodes(c, b) {
    function a(a, b) {
        for (var c = !1, d = 0; d < a.length; d++)
            if (a[d].nodeId == b) {
                c = !0;
                break
            }
        return c
    }
    for (var d = [], e = 0; e < b.length; e++) {
        var g = b[e];
        a(c, g.sourceNode.nodeId) && a(c, g.targetNode.nodeId) && d.push(g)
    }
    return d
}
function filterNodesByLinks(c, b) {
    for (var a = [], d = 0; d < c.length; d++) {
        for (var e = c[d], g = e.nodeId, f = !1, h = 0; h < b.length; h++) {
            var k = b[h];
            if (k.sourceNode.nodeId == g || k.targetNode.nodeId == g) {
                f = !0;
                break
            }
        }
        f && a.push(e)
    }
    return a
}
function getGraphNode(c, b) {
    for (var a = null, d = 0; d < b.length; d++)
        if (b[d].nodeId == c) {
            a = b[d];
            break
        }
    return a
}
function getSubNodes(c, b) {
    var a = []
      , d = c.nodeId;
    c = c.layout.level;
    for (var e = 0; e < b.length; e++) {
        var g = b[e];
        g.sourceNode.nodeId == d && g.targetNode.layout.level == c + 1 && a.push(g.targetNode);
        g.targetNode.nodeId == d && g.sourceNode.layout.level == c + 1 && a.push(g.sourceNode)
    }
    return a = uniqeByKeys(a, ["nodeId"])
}
function filterNodesByLevel(c, b) {
    var a = [];
    b.forEach(function(b) {
        b.layout.level <= c && a.push(b)
    });
    return a
}
function filterNodesByStatus(c, b) {
    if ("all" == c)
        return b;
    for (var a = [], d = 0; d < b.length; d++) {
        var e = b[d];
        ("Company" == e.data.obj.labels && e.data.obj.properties.status == c || e.nodeId == _rootNode.nodeId) && a.push(e)
    }
    return a
}
function filterNodesByStockNum(c, b) {
    for (var a = [], d = 0; d < b.length; d++)
        c == b[d].data.obj.properties.stockPercent && a.push(b[d]);
    return a
}
function filterNodesByInvest(c, b, a) {
    function d(a, b) {
        for (var c = [], d = 0; d < b.length; d++) {
            var e = b[d];
            e.sourceNode.nodeId == a && "INVEST" == e.data.obj.type && c.push(e.targetNode)
        }
        return c
    }
    function e(a, b) {
        for (var c = [], d = 0; d < b.length; d++) {
            var e = b[d];
            e.targetNode.nodeId == a && "INVEST" == e.data.obj.type && c.push(e.sourceNode)
        }
        return c
    }
    function g(a, b) {
        for (var c = [], d = 0; d < b.length; d++) {
            var e = b[d];
            e.targetNode.nodeId == a && "INVEST" == e.data.obj.type && "Person" == e.sourceNode.data.obj.labels[0] && c.push(e.sourceNode)
        }
        return c
    }
    var f = [];
    switch (c) {
    case "all":
        return b;
    case "direct":
        f = d(_rootNode.nodeId, a);
        break;
    case "stockholder":
        c = [];
        b = e(_rootNode.nodeId, a);
        for (f = 0; f < b.length; f++)
            c = c.concat(d(b[f].nodeId, a));
        f = b.concat(c);
        break;
    case "legal":
        c = [];
        b = g(_rootNode.nodeId, a);
        for (f = 0; f < b.length; f++)
            c = c.concat(d(b[f].nodeId, a));
        f = b.concat(c)
    }
    f = f.concat(_rootNode);
    return f = uniqeByKeys(f, ["nodeId"])
}
function filter(c) {
    var b = [];
    (function(a) {
        for (var b = [], c = 0; c < a.nodes.length; c++)
            b.push(a.nodes[c]);
        for (var g = [], c = 0; c < a.links.length; c++)
            g.push(a.links[c]);
        var f = $("#SelPanel").attr("param-level")
          , h = $("#SelPanel").attr("param-status")
          , c = $("#SelPanel").attr("param-num");
        a = $("#SelPanel").attr("param-invest");
        f = parseInt(f) + 1;
        b = filterNodesByLevel(f, b);
        h && (b = filterNodesByStatus(h, b));
        f = [];
        if (c && 0 != c) {
            g = filterLinksByNodes(b, g);
            g = filterNodesByStockNum(c, g);
            for (c = 0; c < g.length; c++)
                f.push(g[c].sourceNode),
                f.push(g[c].targetNode);
            b = uniqeByKeys(f, ["nodeId"])
        }
        a && (b = filterNodesByInvest(a, b, g));
        var k = [];
        b.forEach(function(a, c) {
            c = b;
            var d = g
              , e = !1
              , f = a.layout.level - 1;
            if (2 > f)
                c = !0;
            else {
                for (var h = 0; h < d.length; h++) {
                    var l = d[h];
                    if (l.sourceNode.nodeId == a.nodeId && l.targetNode.layout.level == f && isNodeExist(l.targetNode.nodeId, c)) {
                        e = !0;
                        break
                    }
                    if (l.targetNode.nodeId == a.nodeId && l.sourceNode.layout.level == f && isNodeExist(l.sourceNode.nodeId, c)) {
                        e = !0;
                        break
                    }
                }
                c = e
            }
            c && k.push(a)
        });
        g = filterLinksByNodes(k, g);
        return {
            links: g,
            nodes: k
        }
    }
    )(c).nodes.forEach(function(a) {
        b.push(a.nodeId)
    });
    highLightFilter(b, cy)
}
function filterReset() {
    $("#SelPanel").attr("param-level", "2");
    $("#SelPanel").attr("param-status", "");
    $("#SelPanel").attr("param-num", "");
    $("#SelPanel").attr("param-invest", "");
    $("#ShowLevel a").removeClass("active");
    $("#ShowLevel a").eq(1).addClass("active");
    $("#ShowStatus a").removeClass("active");
    $("#ShowStatus a").eq(0).addClass("active");
    $("#ShowInvest a").removeClass("active");
    $("#ShowInvest a").eq(0).addClass("active");
    $("#inputRange").val(0);
    $("#inputRange").css({
        backgroundSize: "0% 100%"
    })
}
function printLogoFixed() {
    var c = $("body").height()
      , b = $(".printLogo img").height()
      , c = (parseFloat(c) - parseFloat(b)) / 2;
    $(".printLogo img").css({
        "margin-top": c + "px"
    })
}
function selPanelShow() {
    $(".tp-sel").fadeIn();
    $("#TrSel").addClass("active")
}
function selPanelHide() {
    $(".tp-sel").fadeOut();
    $("#TrSel").removeClass("active")
}
function selPanelUpdateList(c, b, a) {
    $(".tp-list").html("");
    for (b = 0; b < c.length; b++) {
        var d = c[b]
          , e = b + 1
          , g = d.data.obj.properties.name
          , f = d.data.obj.properties.keyNo
          , h = ""
          , h = a ? '<div class="checkbox" node_id="' + d.nodeId + '" keyno="' + f + '"> <input checked type="checkbox"><label> ' + e + "." + g + "</label> </div>" : '<div class="checkbox" node_id="' + d.nodeId + '" keyno="' + f + '"><label> ' + e + "." + g + "</label> </div>";
        $(".tp-list").append(h)
    }
    $(".tp-list > div > label").click(function() {
        var a = $(this).parent().attr("node_id");
        focusReady(getGraphNode(a, c))
    });
    $(".tp-list > div > input").click(function() {
        var a = [];
        $(".tp-list input:checked").each(function() {
            var b = $(this).parent().attr("node_id");
            a.push(b)
        });
        highLight(a, cy)
    })
}
function focusReady(c) {
    filterReset();
    $("#FocusInput").val(c.data.obj.properties.name);
    $("#FocusInput").attr("node_id", c.nodeId);
    $("#FocusBt").text("\u805a\u7126");
    $("#FocusBt").removeClass("focusDisable");
    $("#ClearInput").show()
}
function focusCancel() {
    $("#ClearInput").hide();
    $("#FocusBt").text("\u805a\u7126");
    $("#FocusBt").addClass("focusDisable");
    $("#FocusInput").val("");
    $("#FocusInput").attr("node_id", "");
    selPanelUpdateList(_rootData.nodes, _rootData.links, !0);
    cancelHighLight()
}
function maoScale(c) {
    var b = cy.zoom();
    1 == c ? b += .2 : 2 == c && (b -= .2);
    cy.zoom({
        level: b
    })
}
function resizeScreen() {
    isFullScreen() ? ($("#TrFullScreen").addClass("active"),
    $("#TrFullScreen").html('<span class="screen2ed"></span>\u9000\u51fa')) : ($("#TrFullScreen").removeClass("active"),
    $("#TrFullScreen").html('<span class="screen2"></span>\u5168\u5c4f'))
}
function isFullScreen() {
    return document.fullscreen ? !0 : document.mozFullScreen ? !0 : document.webkitIsFullScreen ? !0 : document.msFullscreenElement ? !0 : !1
}
function launchFullScreen(c) {
    c.requestFullscreen ? c.requestFullscreen() : c.mozRequestFullScreen ? c.mozRequestFullScreen() : c.webkitRequestFullscreen ? c.webkitRequestFullscreen() : c.msRequestFullscreen && c.msRequestFullscreen()
}
function exitFullScreen() {
    document.exitFullscreen ? document.exitFullscreen() : document.mozCancelFullScreen ? document.mozCancelFullScreen() : document.msExitFullscreen ? document.msExitFullscreen() : document.webkitCancelFullScreen && document.webkitCancelFullScreen()
}
function toggleText() {
    $("#TrTxt").hasClass("active") ? ($("#TrTxt").removeClass("active"),
    cy.collection("edge").removeClass("edgeShowText")) : ($("#TrTxt").addClass("active"),
    cy.collection("edge").addClass("edgeShowText"))
}
function drawGraph(c) {
    _currentKeyNo;
    _companyRadius = 35;
    _personRadius = 15;
    _circleMargin = 10;
    _circleBorder = 3;
    cy = cytoscape({
        container: document.getElementById("MainCy"),
        motionBlur: !1,
        textureOnViewport: !1,
        wheelSensitivity: .1,
        elements: c,
        minZoom: .4,
        maxZoom: 2.5,
        layout: {
            name: "preset",
            componentSpacing: 40,
            nestingFactor: 12,
            padding: 10,
            edgeElasticity: 800,
            stop: function(a) {
                _isNeedReload = "hidden" == document[state] ? !0 : !1;
                setTimeout(function() {
                    "hidden" == document[state] ? (_isGraphLoaded = !1,
                    console.log("stop _isGraphLoaded=false")) : _isGraphLoaded = !0
                }, 1E3)
            }
        },
        style: [{
            selector: "node",
            style: {
                shape: "ellipse",
                width: function(a) {
                    return "Company" == a.data("type") ? 60 : 45
                },
                height: function(a) {
                    return "Company" == a.data("type") ? 60 : 45
                },
                "background-color": function(a) {
                    return a.data("color")
                },
                "border-color": function(a) {
                    return a.data("borderColor")
                },
                "border-width": 1,
                "border-opacity": 1,
                label: function(a) {
                    a = a.data("name");
                    var b = a.length;
                    return 5 >= b ? a : 5 <= b && 9 >= b ? a.substring(0, b - 5) + "\n" + a.substring(b - 5, b) : 9 <= b && 13 >= b ? a.substring(0, 4) + "\n" + a.substring(4, 9) + "\n" + a.substring(9, 13) : a.substring(0, 4) + "\n" + a.substring(4, 9) + "\n" + a.substring(9, 12) + ".."
                },
                "z-index-compare": "manual",
                "z-index": 20,
                color: "#fff",
                padding: function(a) {
                    return "Company" == a.data("type") ? 3 : 0
                },
                "font-size": 12,
                "font-family": "microsoft yahei",
                "text-wrap": "wrap",
                "text-max-width": 60,
                "text-halign": "center",
                "text-valign": "center",
                "overlay-color": "#fff",
                "overlay-opacity": 0,
                "background-opacity": 1,
                "text-margin-y": function(a) {
                    return "Company" == a.data("type") ? 4 : 2
                }
            }
        }, {
            selector: "edge",
            style: {
                "line-style": function(a) {
                    return "solid"
                },
                "curve-style": "bezier",
                "control-point-step-size": 20,
                "target-arrow-shape": "triangle-backcurve",
                "target-arrow-color": function(a) {
                    return a.data("color")
                },
                "arrow-scale": .5,
                "line-color": function(a) {
                    return a.data("color")
                },
                label: function(a) {
                    return ""
                },
                "text-opacity": .8,
                "font-size": 12,
                "background-color": function(a) {
                    return "#ccc"
                },
                width: .3,
                "overlay-color": "#fff",
                "overlay-opacity": 0,
                "font-family": "microsoft yahei"
            }
        }, {
            selector: ".autorotate",
            style: {
                "edge-text-rotation": "autorotate"
            }
        }, {
            selector: ".nodeActive",
            style: {
                "border-color": function(a) {
                    return a.data("color")
                },
                "border-width": 10,
                "border-opacity": .5
            }
        }, {
            selector: ".edgeShow",
            style: {
                color: "#999",
                "text-opacity": 1,
                "font-weight": 400,
                label: function(a) {
                    return a.data("label")
                },
                "font-size": 10
            }
        }, {
            selector: ".edgeActive",
            style: {
                "arrow-scale": .8,
                width: 1.5,
                color: "#330",
                "text-opacity": 1,
                "font-size": 12,
                "text-background-color": "#fff",
                "text-background-opacity": .8,
                "text-background-padding": 0,
                "source-text-margin-y": 20,
                "target-text-margin-y": 20,
                "z-index-compare": "manual",
                "z-index": 1,
                "line-color": function(a) {
                    return a.data("color")
                },
                "target-arrow-color": function(a) {
                    return a.data("color")
                },
                label: function(a) {
                    return a.data("label")
                }
            }
        }, {
            selector: ".hidetext",
            style: {
                "text-opacity": 0
            }
        }, {
            selector: ".dull",
            style: {
                "z-index": 1,
                opacity: .2
            }
        }, {
            selector: ".nodeHover",
            style: {
                shape: "ellipse",
                "background-opacity": .9
            }
        }, {
            selector: ".edgeLevel1",
            style: {
                label: function(a) {
                    return a.data("label")
                }
            }
        }, {
            selector: ".edgeShowText",
            style: {
                label: function(a) {
                    return a.data("label")
                }
            }
        }, {
            selector: ".lineFixed",
            style: {
                "overlay-opacity": 0
            }
        }]
    });
    cy.on("click", "node", function(a) {
        if (20 == a.target._private.style["z-index"].value)
            if (_isFocus = !0,
            a = a.target,
            highLight([a._private.data.id], cy),
            a.hasClass("nodeActive"))
                activeNode = null,
                $("#company-detail").hide(),
                a.removeClass("nodeActive"),
                cy.collection("edge").removeClass("edgeActive");
            else {
                var b = a._private.data;
                "Company" == b.type ? ($(".tp-detail").show(),
                showDetail(b.keyNo, "company_muhou3"),
                cy.collection("node").addClass("nodeDull")) : $(".tp-detail").hide();
                activeNode = a;
                cy.collection("node").removeClass("nodeActive");
                cy.collection("edge").removeClass("edgeActive");
                a.addClass("nodeActive");
                a.neighborhood("edge").removeClass("opacity");
                a.neighborhood("edge").addClass("edgeActive");
                a.neighborhood("edge").connectedNodes().removeClass("opacity")
            }
        else
            _isFocus = !1,
            activeNode = null,
            cy.collection("node").removeClass("nodeActive"),
            $(".tp-detail").fadeOut(),
            cancelHighLight()
    });
    var b = null;
    cy.on("mouseover", "node", function(a) {
        if (20 == a.target._private.style["z-index"].value) {
            $("#Main").css("cursor", "pointer");
            var c = a.target;
            c.addClass("nodeHover");
            _isFocus || (cy.collection("edge").removeClass("edgeShow"),
            cy.collection("edge").removeClass("edgeActive"),
            c.neighborhood("edge").addClass("edgeActive"));
            clearTimeout(b);
            if (13 < c._private.data.name.length || c._private.data.keyNo && "p" == c._private.data.keyNo[0] && 3 < c._private.data.name.length)
                b = setTimeout(function() {
                    var b = a.originalEvent || window.event
                      , b = "<div class='tips' style='font-size:12px;background:white;box-shadow:0px 0px 3px #999;border-radius:1px;opacity:1;padding:1px;padding-left:8px;padding-right:8px;display:none;position: absolute;left:" + (b.clientX + 10) + "px;top:" + (b.clientY + 10) + "px;'>" + c._private.data.name + "</div>";
                    $("body").append($(b));
                    $(".tips").fadeIn()
                }, 600)
        }
    });
    cy.on("mouseout", "node", function(a) {
        $("#Main").css("cursor", "default");
        $(".tips").fadeOut(function() {
            $(".tips").remove()
        });
        clearTimeout(b);
        a.target.removeClass("nodeHover");
        _isFocus || cy.collection("edge").removeClass("edgeActive")
    });
    cy.on("mouseover", "edge", function(a) {
        _isFocus || (a = a.target,
        cy.collection("edge").removeClass("edgeActive"),
        a.addClass("edgeActive"))
    });
    cy.on("mouseout", "edge", function(a) {
        _isFocus || (a.target.removeClass("edgeActive"),
        activeNode && activeNode.neighborhood("edge").addClass("edgeActive"))
    });
    cy.on("vmousedown", "node", function(a) {
        a = a.target;
        _isFocus || highLight([a._private.data.id], cy)
    });
    cy.on("tapend", "node", function(a) {
        _isFocus || cancelHighLight()
    });
    cy.on("click", "edge", function(a) {
        _isFocus = !1;
        activeNode = null;
        cy.collection("node").removeClass("nodeActive");
        $(".tp-detail").fadeOut();
        cancelHighLight()
    });
    cy.on("click", function(a) {
        a.target === cy && (_isFocus = !1,
        activeNode = null,
        cy.collection("node").removeClass("nodeActive"),
        $(".tp-detail").fadeOut(),
        cancelHighLight(),
        focusCancel(),
        filterReset())
    });
    cy.on("zoom", function() {
        .5 > cy.zoom() ? (cy.collection("node").addClass("hidetext"),
        cy.collection("edge").addClass("hidetext")) : (cy.collection("node").removeClass("hidetext"),
        cy.collection("edge").removeClass("hidetext"));
        setTimeout(function() {
            cy.collection("edge").removeClass("lineFixed");
            cy.collection("edge").addClass("lineFixed")
        }, 200)
    });
    cy.on("pan", function() {
        setTimeout(function() {
            cy.collection("edge").removeClass("lineFixed");
            cy.collection("edge").addClass("lineFixed")
        }, 200)
    });
    cy.nodes().positions(function(a, b) {
        a._private.data.keyNo == _currentKeyNo && (b = cy.pan(),
        cy.pan({
            x: b.x - a._private.data.d3x,
            y: b.y - a._private.data.d3y
        }));
        return {
            x: a._private.data.d3x,
            y: a._private.data.d3y
        }
    });
    cy.ready(function() {
        $("#TrTxt").hasClass("active") || $("#TrTxt").click();
        cy.zoom({
            level: 1.0000095043745896
        });
        $("#load_data").hide();
        setTimeout(function() {
            cy.collection("edge").addClass("lineFixed")
        }, 400)
    });
    cy.nodes(function(a) {})
}
function highLight(c, b) {
    b.collection("node").removeClass("nodeActive");
    b.collection("edge").removeClass("edgeActive");
    b.collection("node").addClass("dull");
    b.collection("edge").addClass("dull");
    for (var a = 0; a < c.length; a++) {
        var d = c[a];
        b.nodes(function(a) {
            a._private.data.id == d && (a.removeClass("dull"),
            a.neighborhood("edge").removeClass("dull"),
            a.neighborhood("edge").addClass("edgeActive"),
            a.neighborhood("edge").connectedNodes().removeClass("dull"))
        })
    }
}
function highLightFilter(c, b) {
    function a(a) {
        for (var b = 0; b < c.length; b++)
            if (a == c[b])
                return !0;
        return !1
    }
    b.collection("node").removeClass("nodeActive");
    b.collection("edge").removeClass("edgeActive");
    b.collection("node").addClass("dull");
    b.collection("edge").addClass("dull");
    for (var d = 0; d < c.length; d++) {
        var e = c[d];
        b.nodes(function(a) {
            a._private.data.id == e && a.removeClass("dull")
        })
    }
    b.edges(function(b) {
        var c = b._private.data;
        a(c.target) && a(c.source) && (b.removeClass("dull"),
        b.addClass("edgeActive"))
    })
}
function cancelHighLight() {
    cy.collection("node").removeClass("nodeActive");
    cy.collection("edge").removeClass("edgeActive");
    cy.collection("node").removeClass("dull");
    cy.collection("edge").removeClass("dull")
}
function getD3Position(c) {
    function b(a) {
        for (var b = [], c = 0; c < a.links.length; c++) {
            var d = a.links[c]
              , e = d.sourceNode.layout.level
              , f = d.targetNode.layout.level;
            (1 == e && 2 == f || 2 == e && 1 == f) && b.push(d);
            (2 == e && 3 == f || 3 == e && 2 == f) && b.push(d)
        }
        b.forEach(function(a, c) {
            3 == a.targetNode.layout.level && b.forEach(function(c, d) {
                c.linkId == a.linkId || c.targetNode.nodeId != a.targetNode.nodeId && c.sourceNode.nodeId != a.targetNode.nodeId || b.splice(d, 1)
            });
            3 == a.sourceNode.layout.level && b.forEach(function(c, d) {
                c.linkId == a.linkId || c.targetNode.nodeId != a.sourceNode.nodeId && c.sourceNode.nodeId != a.sourceNode.nodeId || b.splice(d, 1)
            })
        });
        return b
    }
    getLayoutNode(c);
    (function(a) {
        function c(a, b) {
            for (var c = 0, d = 0; d < b.length; d++)
                if (a == b[d].nodeId) {
                    c = d;
                    break
                }
            return c
        }
        for (var d = 0; d < a.nodes.length; d++) {
            var e = a.nodes[d];
            e.id = e.nodeId
        }
        for (d = 0; d < a.links.length; d++)
            e = a.links[d],
            e.source = c(e.sourceNode.nodeId, a.nodes),
            e.target = c(e.targetNode.nodeId, a.nodes),
            e.index = d;
        a.layoutLinks = b(a);
        setSingleLinkNodes(a.layoutLinks);
        a.nodes.forEach(function(a, b) {
            a.layout.singleLinkChildren.length && _maxChildrenLength < a.layout.singleLinkChildren.length && (_maxChildrenLength = a.layout.singleLinkChildren.length)
        })
    }
    )(c);
    var a = $("#MainD3 svg").width()
      , d = $("#MainD3 svg").height()
      , e = -600
      , g = 330
      , f = 0
      , h = 130
      , k = 35;
    50 > c.nodes.length ? (e = -800,
    g = 400) : 50 < c.nodes.length && 100 > c.nodes.length ? (e = -800,
    g = 350,
    h = 130,
    k = 35) : 100 < c.nodes.length && 150 > c.nodes.length ? (e = -900,
    g = 450) : 150 < c.nodes.length && 200 > c.nodes.length ? (e = -1E3,
    g = 500) : 200 < c.nodes.length && (e = -1600,
    g = 500,
    f = .6,
    h = 100,
    k = 35);
    50 < _maxChildrenLength && 100 > _maxChildrenLength ? (e = -2E3,
    g = 500) : 1E3 < _maxChildrenLength && 2E3 > _maxChildrenLength && (e = -4E3,
    g = 1500);
    console.log(c);
    d3.forceSimulation(c.nodes).force("charge", d3.forceManyBody().strength(e).distanceMax(g).theta(f)).force("link", d3.forceLink(c.layoutLinks).distance(h)).force("center", d3.forceCenter(a / 2, d / 2)).force("collide", d3.forceCollide().radius(function() {
        return k
    }))
}
function getLayoutNode(c) {
    var b = {
        current: _rootNode,
        level1: [],
        level2: [],
        level3: [],
        level4: [],
        level5: [],
        other: []
    };
    c.nodes.forEach(function(a, c) {
        switch (a.layout.level) {
        case 1:
            b.level1.push(a);
            break;
        case 2:
            b.level2.push(a);
            break;
        case 3:
            b.level3.push(a);
            break;
        case 4:
            b.level4.push(a);
            break;
        case 5:
            b.level5.push(a);
            break;
        default:
            b.other.push(a)
        }
    });
    return _layoutNode = b
}
function transformData(c) {
    id = c.nodes[0].nodeId;
    var b = {
        nodes: [],
        edges: []
    };
    c.links.forEach(function(a, c) {
        c = a.data.obj.type;
        c = "INVEST" == c ? _COLOR.line.invest : "EMPLOY" == c ? _COLOR.line.employ : "LEGAL" == c ? _COLOR.line.legal : void 0;
        var d = a.data.obj.type
          , g = a.data.obj.properties.role;
        b.edges.push({
            data: {
                data: a.data,
                color: c,
                id: a.linkId,
                label: "INVEST" == d ? "\u6295\u8d44" : "EMPLOY" == d ? g ? g : "\u4efb\u804c" : "LEGAL" == d ? "\u6cd5\u5b9a\u4ee3\u8868\u4eba" : void 0,
                source: a.sourceNode.nodeId,
                target: a.targetNode.nodeId
            },
            classes: "autorotate"
        })
    });
    c.nodes.forEach(function(a) {
        b.nodes.push({
            data: {
                nodeId: a.nodeId,
                type: a.data.obj.labels[0],
                keyNo: a.data.obj.properties.keyNo,
                data: a.data,
                id: a.nodeId,
                name: a.data.obj.properties.name,
                category: a.data.category,
                color: a.data.color,
                borderColor: a.data.strokeColor,
                layout: a.layout,
                d3x: a.x,
                d3y: a.y
            }
        })
    });
    return b
}
function domUpdate(c) {
    getD3Position(c);
    setTimeout(function() {
        drawGraph(transformData(c))
    }, 500);
    selPanelUpdateList(c.nodes, c.links, !0)
}
function downImg(c) {
    c = c.replace(function(a) {
        a = a.toLocaleLowerCase().replace(/jpg/i, "jpeg");
        return "image/" + a.match(/png|jpeg|bmp|gif/)[0]
    }("png"), "image/octet-stream");
    var b = (new Date).toLocaleDateString() + ".png";
    (function(a, b) {
        var c = document.createElement("a");
        c.href = a;
        c.download = b;
        a = document.createEvent("MouseEvents");
        a.initMouseEvent("click", !0, !1, window, 0, 0, 0, 0, 0, !1, !1, !1, !1, 0, null);
        c.dispatchEvent(a)
    }
    )(c, b)
}
function downloadimgIE(c) {
    var b = 1;
    3E3 < c.width ? b = .5 : 5E3 < c.width && (b = .4);
    b = c.toDataURL("image/jpeg", b);
    c = INDEX_URL + "cms_downloadimg?filename=" + (_FILENAME + "\u7684\u5173\u8054\u56fe\u8c31.png");
    var b = {
        img: b
    }
      , a = document.createElement("form");
    a.action = c;
    a.enctype = "multipart/form-data";
    a.method = "post";
    a.style.display = "none";
    for (var d in b)
        c = document.createElement("textarea"),
        c.name = d,
        c.value = b[d],
        a.appendChild(c);
    document.body.appendChild(a);
    a.submit()
}
function canvasImg(c) {
    var b = new Image;
    b.onload = function(a) {
        a = document.createElement("canvas");
        a.width = b.width;
        a.height = b.height;
        var c = a.getContext("2d");
        c.fillStyle = "#fff";
        c.fillRect(0, 0, a.width, a.height);
        c.drawImage(b, 0, 0);
        400 < a.width && (c.font = "28px \u5fae\u8f6f\u96c5\u9ed1",
        c.fillStyle = "#aaaaaa",
        c.fillText("\u5173\u8054\u56fe\u8c31\u7531\u4f01\u67e5\u67e5\u57fa\u4e8e\u516c\u5f00\u4fe1\u606f\u5229\u7528\u5927\u6570\u636e\u5206\u6790\u5f15\u64ce\u72ec\u5bb6\u751f\u6210", a.width / 2 - c.measureText("\u5173\u8054\u56fe\u8c31\u7531\u4f01\u67e5\u67e5\u57fa\u4e8e\u516c\u5f00\u4fe1\u606f\u5229\u7528\u5927\u6570\u636e\u5206\u6790\u5f15\u64ce\u72ec\u5bb6\u751f\u6210").width / 2, a.height - 30));
        var e = new Image;
        e.src = "/material/theme/chacha/cms/v2/images/shuiying.png";
        320 < a.width ? c.drawImage(e, a.width / 2 - 160, a.height / 2 - 80, 320, 160) : c.drawImage(e, a.width / 2 - 80, a.height / 2 - 40, 160, 80);
        downloadimgIE(a)
    }
    ;
    b.src = c
}
function getData(c, b) {
    b = $.extend({
        keyNo: c
    }, b);
    $("#load_data").show();
    $.ajax({
        url: INDEX_URL + "/company_muhouAction",
        type: "GET",
        data: b,
        dataType: "JSON",
        success: function(a) {
            (a = a.success) && void 0 != a.results && a.results[0] && a.results[0].data.length && 0 != a.results[0].data[0].graph.nodes.length ? ($(".printLogo").show(),
            $(".tp-foot").show(),
            $("#Main").show(),
            $("#no_data").hide(),
            _rootData = getRootData(a.results[0].data),
            domUpdate(_rootData)) : ($("#load_data").hide(),
            $(".printLogo").hide(),
            $(".tp-foot").hide(),
            $("#Main").hide(),
            $("#no_data").show())
        },
        error: function(a) {
            $("#load_data").hide();
            $(".printLogo").hide();
            $(".tp-foot").hide();
            $("#Main").hide();
            $("#no_data").show()
        }
    })
}
window.onresize = function() {
    resizeScreen();
    printLogoFixed()
}
;
$(document).ready(function() {
    printLogoFixed();
    _currentKeyNo = getQueryString("keyNo");
    getData(_currentKeyNo);
    $("#ShowLevel > a").click(function() {
        $("#ShowLevel > a").removeClass("active");
        $(this).addClass("active");
        var b = parseInt($(this).attr("level"));
        $("#SelPanel").attr("param-level", b);
        filter(_rootData)
    });
    $("#ShowStatus > a").click(function() {
        $("#ShowStatus > a").removeClass("active");
        $(this).addClass("active");
        var b = $(this).attr("status");
        $("#SelPanel").attr("param-status", b);
        filter(_rootData)
    });
    var c = window.ActiveXObject || "ActiveXObject"in window ? "change" : "input";
    $("#inputRange").bind(c, function(b) {
        b = $("#inputRange").val();
        $("#rangeValue").text(b);
        $("#inputRange").css("background-size", b + "% 100%");
        $("#RangeLabel span").text(b + "%");
        $("#SelPanel").attr("param-num", b);
        filter(_rootData)
    });
    $("#ShowInvest > a").click(function() {
        $("#ShowInvest > a").removeClass("active");
        $(this).addClass("active");
        var b = $(this).attr("invest");
        $("#SelPanel").attr("param-invest", b);
        filter(_rootData)
    });
    $(".tp-sel-close span").click(function() {
        selPanelHide()
    });
    $("#FocusBt").click(function() {
        var b = $("#FocusBt").text();
        if (!$(this).hasClass("focusDisable"))
            if ("\u805a\u7126" == b)
                if ($("#FocusInput").val()) {
                    if (b = $("#FocusInput").attr("node_id"))
                        $("#FocusBt").text("\u53d6\u6d88"),
                        highLight([b], cy)
                } else
                    faldia({
                        content: "\u8bf7\u70b9\u51fb\u9009\u53d6\u7ed3\u70b9"
                    });
            else
                "\u53d6\u6d88" == b && focusCancel()
    });
    $("#FocusInput").keyup(function() {
        $(".tp-list").html("");
        var b = $(this).val();
        b ? $("#ClearInput").show() : $("#ClearInput").hide();
        setTimeout(function() {
            var a = [];
            _rootData.nodes.forEach(function(c) {
                c.data.obj.properties.name.match(b) && a.push(c)
            });
            selPanelUpdateList(a, _rootData.links, !1)
        }, 500)
    });
    $("#ClearInput").click(function() {
        focusCancel()
    });
    $(".tp-detail-close span").click(function() {
        $(".tp-detail").fadeOut()
    });
    $("#TrSel").click(function() {
        $(this).hasClass("active") ? selPanelHide() : selPanelShow()
    });
    $("#TrFullScreen").click(function() {
        var b = cy.pan();
        isFullScreen() ? (cy.pan({
            x: b.x,
            y: b.y - 60
        }),
        exitFullScreen()) : (cy.pan({
            x: b.x,
            y: b.y + 60
        }),
        launchFullScreen($("#Main")[0]))
    });
    $("#TrRefresh").click(function() {
        $("#TrTxt").removeClass("active");
        getData(_currentKeyNo);
        focusCancel();
        filterReset()
    });
    $("#TrSave").click(function() {
        $("#TrTxt").hasClass("active") || $("#TrTxt").click();
        canvasImg(cy.png({
            full: !0,
            bg: "#0000",
            scale: 1.8
        }))
    })
});
