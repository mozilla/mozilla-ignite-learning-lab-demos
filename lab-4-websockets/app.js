var express = require("express");
var io = require('socket.io');
var app = express(),
    server = require('http').createServer(app),
    io = io.listen(server);

var csv = require('csv');
var fs = require('fs');

server.listen(8080);

// Set up place for static files
app.use("/public", express.static(__dirname + '/public'));

app.get('/', function (req, res) {
    res.sendfile(__dirname + '/index.html');
});

io.set('log level', 0);

io.sockets.on('connection', function (socket) {

    // Make sure once the stream is started,
    //  it can't be restarted
    var started = false;
    var _frameSize = 100;

    socket.on('startStream', function (data) {

        // Check the flag
        if (started){
            return;
        }
        else{
            started = true;
        }

        var path = __dirname + '/datasets/1-percent/frames.csv';

        // The current frame count
        var count = 0;

        // The frame buffer, which holds the data
        var rows = [];

        console.log('Beginning frame sending');

        socket.on('streamdatachanged', function (data) {
            // All the frames should at least have 10,000 lines
            // But this is a temporary hack.
            var stringified = '' + data.percent * 10000;
            _frameSize = +stringified.split('.')[0];
        });

        fs.readFile(path, 'utf-8', function (err, data) {
            var lines = data.split('\n'),
                numLines,
                baseCase,
                frameSize = lines.indexOf('eof');

            _frameSize = numLines = baseCase = frameSize;

            csv().fromPath(path).on('data', function (data, index) {

                // Since all frames are in a single CSV for the highest performance,
                // check for the 'end of frame'
                if (data[0] === 'eof') {

                    // If it's the end of the frame, send it off
                    socket.emit('frame', {
                        index: count,
                        frame: rows
                    });

                    console.log('Sending frame #' + count);

                    // housework
                    count++;
                    numLines = _frameSize;
                    rows = [];
                }

                // If it's not the end of frame, add it to the row buffer
                //rows.push(data);

                if (numLines > 0) {
                    numLines--;
                    rows.push(data);
                }

            }).on('end', function () {
                socket.emit('done', {
                    message: 'Done sending frames',
                    count: count
                })
                console.log('Done sending frames')
            });
        });
    });
});
