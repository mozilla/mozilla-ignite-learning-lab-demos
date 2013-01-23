var express = require('express');
var app = express();
var engines = require('consolidate');

// Register Handlebars ar our template engine
app.engine('html', engines.hogan);
app.set('view engine', 'html');
app.set('views', __dirname + '/assets');

app.get('/', function(req, res) {
	res.render('index', {});
});

app.get('/css/general.css', function(req, res) {
	res.sendfile(__dirname + '/assets/css/general.css');
});

app.get('/js/general.js', function(req, res) {
	res.sendfile(__dirname + '/assets/js/general.js');
});

app.listen(8000);
console.log('Running SPDY demo on port 8000');