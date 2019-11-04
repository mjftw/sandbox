module.exports = function(RED) {
    const { exec } = require('child_process');
    var fs = require('fs');

    function screenshot(config) {
        RED.nodes.createNode(this, config);

        var context = this.context();
        var node = this;

        var filename = 'screenshot.png';

        this.on('input', function(msg) {
            var err = null;

            exec('fbgrab '.concat(filename), function(err, complete) {
                if(err) {
                    node.error(err);
                    err = -1;
                }
            });

            if(err) {
                node.error('Screenshot failed');
                return;
            }

            var img_data = null;
            fs.readFile(filename, function(err, data) {
                if(err) {
                    node.error(err)
                }
                else {
                    var outMsg = {payload: data};
                    node.send(outMsg);
                }
            });

            fs.unlink(filename, function(err) {
                if(err) {
                    node.error(err);
                }
            });
        });
    }
    RED.nodes.registerType('Screenshot', screenshot);
}