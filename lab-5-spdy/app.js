var express = require('express');
var app = express();
var engines = require('consolidate');
var spdy = require('spdy');
var https = require('https');
var fs = require('fs');

// Register Handlebars ar our template engine
app.engine('html', engines.hogan);
app.set('view engine', 'html');
app.set('views', __dirname + '/assets');
app.use(express.bodyParser());

// Set up the different URLs we will be using
app.get('/', function(req, res) {

	res.render('index', {
		host: req.host,
		spdyEnabled: false,
	});

});

// Randomly generate some intergers so we're sure not to cache the images
app.post('/', function(req, res) {

	// Set up our cols
	var columns = {2: [], 3: [], 4:[], 5:[]};

	for (var i = req.body.images_to_load; i > 0; i--) {

		// Divide the across the cols and give it a random height
		var rand = getRandomInt(1000000, 9999999);
		columns[i % 4 + 2].push({
			rand: rand,
			height: 50 * (rand % 5 + 1),
		});

	}

	res.render('index', {
		imagesToLoad: req.body.images_to_load,
		spdyEnabled: (typeof req.body.spdy_enabled === 'undefined' ? false : true),
		columns: columns,
		host: req.host,
	});

});

app.get('/css/general.css', function(req, res) {
	res.sendfile(__dirname + '/assets/css/general.css');
});

app.get('/js/general.js', function(req, res) {
	res.sendfile(__dirname + '/assets/js/general.js');
});

app.get('/images/logo.png', function(req, res) {
	res.sendfile(__dirname + '/assets/images/logo.png');
});

// Retrieve our keys for our HTTPS connection
var options = {
	key: fs.readFileSync(__dirname + '/keys/spdy-key.pem'),
	cert: fs.readFileSync(__dirname + '/keys/spdy-cert.pem'),
}

var httpsServer = https.createServer(options, app);
httpsServer.listen(8000)

// Put another copy of the app up on port 8001, with SPDY enabled.
var spdyOptions = {
	key: options.key,
	cert: options.cert,
	ca: fs.readFileSync(__dirname + '/keys/spdy-csr.pem'),
	windowSize: 1024,
};

var spdyServer = spdy.createServer(spdyOptions, app);
spdyServer.listen(8001);

// Generate a random int betwee two bounds
function getRandomInt(min, max) {
	return Math.floor(Math.random() * (max - min + 1)) + min;
}

console.log('Running SPDY demo on port 8000 and 8001');