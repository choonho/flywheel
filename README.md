# flywheel

This is simple network bandwidth checking tool

## Idea

If you click "Start Speed Test" button, web browser starts to download 2MB image file continuously.
The Server calculates the start time and end time, then calcuate the bandwidth.

# Execute

Web server starts service with TCP 80 port.

~~~bash
python flywheel.py
~~~

# Usage

Open a web browser with http://<server>

# Visualization Tool

Gauge shows the current bandwidth.
LineChart shows the bandwidth history.

# API

Type | URL
---- | ----
GET  | http://<server>/download_image.jpg
GET  | http://<server>/speed
GET  | http://<server>/history



