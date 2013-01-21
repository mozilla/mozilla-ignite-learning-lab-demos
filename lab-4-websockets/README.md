# Mozilla Ignite - Websockets Learning Lab Demo

In this lab we're going to re-examine learning lab #1. That lab used WebGL to render point cloud data that was being streamed from the server. It was mentioned that the data was streamed using a new HTML5 technology called websockets.

In this lab, we're going to focus on the websockets aspect of the lab, showing the full communication between the client and server that is taking place. We show this information via a new console on the bottom of the page.

## Why Was Websockets Necessary?

When the server is asked to start streaming point cloud data, a process takes place:

* A CSV file containing point cloud data is loaded
* The server begins parsing and sending frames one-by-one

Using classic web technologies like AJAX just wouldn't suffice here. We want the client to be able to start rendering frames of point cloud data as soon as possible. With something like ajax, we would either need to:

* Poll the server and ask for each frame or frames
* or deliver the entire point cloud payload in one AJAX request

Both options are messy and bound to cause performance issues on the client side. The best option is to use websockets to send each frame to the client as it is read from the CSV.

## Apparent Bottlenecks and Faster Internet

The bottleneck in achieving a high frame rate (upper left side of the page) has to do with the connection available between the client and server.

We encourage you to try running the server locally, then on a home network, then over the internet. How does the throughput reported at the end of the streaming process change? How are future applications like this severely limited by the availability of high-speed internet?

## Prerequisites

A `node.js` installation, and Chrome or Firefox

## How to Run It

    $ node app.js

Then head to [http://localhost:8080/](http://localhost:8080/)

When the page loads, click "Stream" at the top of the page. At this point, raw pointcloud data will begin streaming from the server to your browser. There may be a short delay while your computer loads and parses the CSV file of pointcloud data, but a 3D rendering of Radiohead's lead singer singing will appear shortly thereafter.

You can control the level of quality using the "StreamData" slider in the upper-right corner. A level of 100 is for perfect detail, while a level of 1 would yield minimal quality.

## License

TBD


