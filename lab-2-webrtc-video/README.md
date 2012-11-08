# Mozilla Ignite - WebRTC Learning Lab Demo
===========================================

This is a project that demonstrates the ability of web browsers to facilitate peer-to-peer audio/video communication via camera/mic access and a native javascript API. At the time of this writing, the only browsers capable of running this is Google Chrome Canary and Firefox nightly (details below).

The purpose of this demo is to show how differing internet connections affect both video quality and the ability to reliably stream to `n` clients, as `n` gets bigger. If gigabit internet connections were available to the average internet user, efficient multi-person face to face could be an implementable feature in any collaborative app.

In addition to the above, explore how *easy* it might be to add audio/video capability to applications like helpdesks, online office suites, etc, when the barriers of browser support and required bandwidth are removed.

If you have the resources, try running this application with multiple friends over the internet and see how and why video quality breaks down at scale.

## Prerequisites

A `node.js` installation, and [Chrome Canary](https://tools.google.com/dlpage/chromesxs) or a [nightly build of Firefox](http://nightly.mozilla.org/).

## How to Run It

    $ node app.js

Then head to [http://localhost:8080/](http://localhost:8080/), and click 'allow' to see your camera.

Then, open another tab (or a browser on another networked computer) and go to http://localhost:8080 or http://hostname:8080. Again, click 'allow', and a connection will be made between your two open windows.

## Credits

This project was adapted from the webrtc.io example project with permission at [https://github.com/webRTC/webrtc.io-demo/](https://github.com/webRTC/webrtc.io-demo/).

Developed by:
    [@dennismatensson](https://github.com/dennismartensson)
    [@cavedweller](https://github.com/cavedweller)
    [@sarenji](https://github.com/sarenji)

Modified by:
	[@katzgrau](https://github.com/katzgrau)

## For more info on how to start developing with webRTC.io

Go to [https://github.com/webRTC/webRTC.io](https://github.com/webRTC/webRTC.io) and read the instructions.