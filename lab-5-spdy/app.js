var express = require('express');
var app = express();

app.get('/', function(req, res) {
	res.sendfile(__dirname + '/assets/index.html');
});

app.get('/css/general.css', function(req, res) {
	res.sendfile(__dirname + '/assets/css/general.css');
});

app.get('/js/general.js', function(req, res) {
	res.sendfile(__dirname + '/assets/js/general.js');
});

app.listen(8000);
console.log('Running SPDY demo on port 8000');