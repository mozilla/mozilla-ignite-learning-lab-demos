/**
 * Mozilla Ignite Learning Labs SPDY Demo
 * General frontend JS
 */

(function($) {

	window.Loader = {

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
		// down the viewport and switching between SPDY and non-SPDY ports
		bindUIActions: function() {

			$('#slider').slider({
				min: 10,
				max: 50,
				create: function(event, ui) {
					$('#slider').slider('value', $('#images-to-load').val());
				},
				change: function(event, ui) {
					$('#images-to-load').val(ui.value);
				}
			});

			$('#spdy-enabled').on('change', function() {
				Loader.switchPort($(this));
			});

			$(window).on('scroll', function() {
				var windowPosition = $(this).scrollTop() + $(this).height();
				var loadAfter = $(document).height() - 10;

				// Are we approaching the bottom of the window yet?
				if (windowPosition > loadAfter) Loader.processForm();
			});

		},

		// Switches the `action` of the form between port 8000 and 8001
		switchPort: function($el) {
			var formSrc = $('form').attr('action');
			var newFormSrc;

			if ($el.is(':checked')) newFormSrc = formSrc.replace('8000', '8001');
			else newFormSrc = formSrc.replace('8001', '8000');

			$('form').attr('action', newFormSrc);
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

				var rand = getRandomInt(1000000, 9999999);

				// Attaching a handler right in the HTML, because this is the
				// only reliable way to deal with onLoad events. See
				// http://stackoverflow.com/a/8570976
				var $el = $('<img />').attr({
					'src': 'http://localhost/large.jpg?rand=' + rand,
					'onload': 'Loader.decrementRemainingImages()',
					'width': 190,
					'height': 50 * (rand % 5 + 1),
				});

				this.appendImage($el);

			}

		},

		// Append the image element to the correct column, preferring
		// shorting columns.
		appendImage: function($el) {

			// Assume the second col is the shortest for now.
			var shortestCol = {
				index: 2,
				height: $('#column-2').height(),
			}

			// Check if any of the cols is even shorter
			$.each([3, 4, 5], function(index, value) {
				colHeight = $('#column-' + value).height();

				if (colHeight < shortestCol.height) {
					shortestCol.index = value;
					shortestCol.height = colHeight;
				}
			});

			var $section = $('<section />').append($el);
			$('#column-' + shortestCol.index).append($section);

		},

		// Decrease our counter and display the loading time if needed.
		decrementRemainingImages: function() {
			this.remainingImages--;
			if (this.remainingImages !== 0) return;

			var deltaMs = Date.now() - this.loadingCycleStart;
			$('.loading-time').text(deltaMs/1000);
			$('.spdy-status').text(this.settings.spdyEnabled ? 'enabled' : 'disabled');

		},

	}

	// Generate a random integer between two bounds
	function getRandomInt(min, max) {
		return Math.floor(Math.random() * (max - min + 1)) + min;
	}

	$(document).ready(function() {
		Loader.init();
	});

	console.log('Welcome to the Mozilla Ignite Learning Labs SPDY Demo')

})(jQuery);