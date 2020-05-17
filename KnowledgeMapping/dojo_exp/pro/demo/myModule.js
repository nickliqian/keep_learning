define([
    // The dojo/dom module is required by this module, so it goes
    // in this list of dependencies.
    // 引入依赖
    'dojo/dom'
], function(dom){
    // Once all modules in the dependency list have loaded, this
    // function is called to define the demo/myModule module.
    //
    // The dojo/dom module is passed as the first argument to this
    // function; additional modules in the dependency list would be
    // passed in as subsequent arguments.

    var oldText = {};

    // This returned object becomes the defined value of this module
    return {
        // 为指定元素赋值
        setText: function (id, text) {
            var node = dom.byId(id);  // 定位元素
            oldText[id] = node.innerHTML;  // 元素内容
            node.innerHTML = text;  // 元素文本赋值
        },

        // 给指定元素恢复之前的值
        restoreText: function (id) {
            var node = dom.byId(id);
            node.innerHTML = oldText[id];
            delete oldText[id];
        }
    };
});