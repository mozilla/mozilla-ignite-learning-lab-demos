var express = require("express");
var io = require('socket.io');
var app = express()
  , server = require('http').createServer(app)
  , io = io.listen(server);

server.listen(8080);

// Load datasets into memory

app.get('/', function (req, res) {
  res.sendfile(__dirname + '/index.html');
});

io.sockets.on('connection', function (socket) {
  
  socket.on('startStream', function(data) {
  	// check quality in parameter
  	if(data.quality > 0) {
  		socket.emit('frame', {frame: 'Mad data'});
  	}

  });
 
});