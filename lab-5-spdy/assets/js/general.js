/**
 * Mozilla Ignite Learning Labs SPDY Demo
 * General frontend JS
 */

(function($) {

	var Loader = {

		settings: {
			spdyEnabled: true,
			imagesToLoad: 20,
		},

		// Images still left to load
		remainingImages: 0,

		// Timestamp when this loading cycle started
		loadingCycleStart: 0,

		// Bootstrap the module
		init: function() {
			this.bindUIActions();
		},

		// Set up events for both submitting the form, as well as scrolling
		// down the viewport
		bindUIActions: function() {

			$('form').on('submit', function(e) {
				e.preventDefault();
				Loader.processForm();
			});

			$(window).on('scroll', function() {
				var windowPosition = $(this).scrollTop() + $(this).height();
				var loadAfter = $(document).height() - 100;

				// Are we approaching the bottom of the window yet?
				if (windowPosition > loadAfter) Loader.processForm();
			});

		},

		// Retrieve our loading settings from the form and put the
		// module in loading state
		processForm: function() {

			// Make sure we're not already loading images
			if (this.remainingImages !== 0) return false;
			$checkbox = $('#spdy-enabled');

			this.settings.spdyEnabled = $checkbox.is(':checked') ? true : false;
			this.settings.imagesToLoad = parseInt($('#images-to-load').val(), 10);
			this.remainingImages = this.settings.imagesToLoad;

			// And off we go!
			this.loadImages();
		},

		// Load the desired amount of images
		loadImages: function() {
			this.loadingCycleStart = Date.now();

			// Decrease our counter for every image we load, so we can keep
			// track of our progress
			for (var i = this.settings.imagesToLoad; i > 0; i--) {

				var rand = getRandomInt();

				// Construct a new image and bind the event. We can safely
				// use the load method, because each image has a random int
				// appended to it and therefore won't be cached.
				var $el = $('<img />').attr('id', rand);
				$('#column-2').append($el);

				$('#' + rand).load(this.checkRemainingImages());
				$('#' + rand).attr('src', 'http://localhost/large.jpg?rand=' + rand);

			}

		},

		checkRemainingImages: function(el) {
			this.remainingImages--;
			if (this.remainingImages === 0) console.log('Finished loading');
		},

	}

	function getRandomInt() {
		var min = 1000000;
		var max = 9999999;
		return Math.floor(Math.random() * (max - min + 1)) + min;
	}


	$(document).ready(function() {
		Loader.init();
	});

	console.log('Welcome to the Mozilla Ignite Learning Labs SPDY Demo')

})(jQuery);