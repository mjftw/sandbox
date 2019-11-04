module.exports = function(RED) {
    function helloWorld(config) {
        RED.nodes.createNode(this, config);

        var context = this.context();
        var node = this;

        this.on('input', function(msg) {
            var outMsg = {payload: 'Hello World'};
            node.send(outMsg);
        });
    }
    RED.nodes.registerType('Hello World', helloWorld);
}