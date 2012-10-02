# Mozilla Ignite - WebGL Learning Lab Demo

This is a demo demonstrating the streaming of 3D point clouds over the wire, and drawing them in the browser using WebGL, with webSockets as the transport mechanism.

The purpose of this demo is to show how differing internet connections have an impact on future applications like this on. Locally, you may be able to view the 3D point cloud at its highest level of details. 

If you throw this application on a remote webserver, you'll watch the level of quality quickly degrade as the bottlenecks of current internet speed may themselves apparent.

## Prerequisites

A `node.js` installation, and Chrome or Firefox

## How to Run It

    $ node app.js

Then head to [http://localhost:8080/](http://localhost:8080/)

When the page loads, click "Stream" at the top of the page. At this point, raw pointcloud data will begin streaming from the server to your browser. There may be a short delay while your computer loads and parses the CSV file of pointcloud data, but a 3D rendering of Radiohead's lead singer singing will appear shortly thereafter.

You can control the level of quality using the "StreamData" slider in the upper-right corner. A level of 100 is for perfect detail, while a level of 1 would yield minimal quality.

## License

TBD


