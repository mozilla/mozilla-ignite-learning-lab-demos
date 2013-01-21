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

		// Are we already busy fetching new images?
		loading: false,

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
			if (this.loading === true) return false;
			
			this.loading = true;
			$checkbox = $('#spdy-enabled');

			this.settings.spdyEnabled = $checkbox.is(':checked') ? true : false;
			this.settings.imagesToLoad = $('#images-to-load').val();
		},

	}

	$(document).ready(function() {
		Loader.init();
	});

	console.log('Welcome to the Mozilla Ignite Learning Labs SPDY Demo')

})(jQuery);