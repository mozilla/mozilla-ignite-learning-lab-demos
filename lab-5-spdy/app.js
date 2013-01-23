var express = require('express');
var app = express();
var engines = require('consolidate');

// Register Handlebars ar our template engine
app.engine('html', engines.hogan);
app.set('view engine', 'html');
app.set('views', __dirname + '/assets');
app.use(express.bodyParser());

app.get('/', function(req, res) {
	res.render('index');
});


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

	res.render('index', {columns: columns});

});


app.get('/css/general.css', function(req, res) {
	res.sendfile(__dirname + '/assets/css/general.css');
});


app.get('/js/general.js', function(req, res) {
	res.sendfile(__dirname + '/assets/js/general.js');
});


app.listen(8000);

// Generate a random int betwee two bounds
function getRandomInt(min, max) {
	return Math.floor(Math.random() * (max - min + 1)) + min;
}

console.log('Running SPDY demo on port 8000');