# Mozilla Ignite - SPDY Learning Lab Demo

This demo shows the speed benefit of using the SPDY protocol over normal HTTP. The SPDY protocol achieves this speed up by prioritizing and multiplexing the transfer of resource, all in a single connection with the client. Requests are compressed by design instead of being optional.

## Prerequisites

A recent version of `node`, Chrome or Firefox. The current version of Google Chrome (24.0.1312.56) sometimes has issues loading the SPDY-enabled demo. You might want to try Google Chrome Canary if you run into this problem.

You can also download an [add-on][1]/[extension][2] for your browser to quickly see whether the page you're currently on has SPDY enabled. You won't need this to use the demo.

[1]: https://addons.mozilla.org/en-us/firefox/addon/spdy-indicator/
[2]: https://chrome.google.com/webstore/detail/spdy-indicator/mpbpobfflnpcgagjijhmgnchggcjblin?hl=en

## How to Run It

    $ node app.js

Then head to [https://localhost:8000/](https://localhost:8000/). You will get an error about an untrusted certificate. Confirm or add the exception in your browser.

You can now drag the slider to indicate how many images you want to load and whether you want to enable SPDY. Hit the 'load' button and the images will be loaded. You can also scroll down to load even more images.

## License

TBD