#!/usr/bin/env python

import os
import time

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from optparse import OptionParser

fp = open('2MB','rb')
output = fp.read()
fp.seek(0, os.SEEK_END)
volume =fp.tell()
fp.close()

current_speed = 0

class myHandler(BaseHTTPRequestHandler):
    # Handler for the GET requests
    def do_GET(self):
        print "GET: %s" % self.path
        if self.path == "/":
            self.main_page()
        elif self.path == "/download_image.jpg":
            self.download_image(10)
        return

    def download_image(self, size):
        """
        make fake image file, and send it to client
        """
        self.send_response(200)
        self.send_header('Content-type','image/jpeg')
        self.send_header('Content-Length',volume)
        self.end_headers()
        # start time
        stime = time.time()
        print "Started at ", stime
        # Send file (Create 10MB contents)
        self.wfile.write(output)
        #self.wfile.write(self.main_page())
        # end time
        etime = time.time()
        print "Ended at ", etime
        elapse = etime - stime
        print "==================== log ==================="
        print "Time: %s" % elapse
        global current_speed
        current_speed = volume * 8 / elapse / 1024 / 1024
        print "Bandwith: %s Mbps" % current_speed
        return


    def main_page(self):
        html = """<html>
<head>
<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<script type="text/javascript">
    google.charts.load('current', {'packages':['gauge']});
    google.charts.setOnLoadCallback(drawChart);
    function drawChart() {
        var data = google.visualization.arrayToDataTable([
            ['Label','Value'],
            ['TCP Download',0]
            ]);
        var options = {
            width:400, height:120,
            redFrom:0, redTo:10,
            yellowFrom:10, yellowTo:20,
            minorTicks: 5
            };
        var chart = new google.visualization.Gauge(document.getElementById('chart_div'));
        chart.draw(data, options);

        setInterval(function() {
            data.setValue(0, 1, %s);
            chart.draw(data, options);
            }, 1000);
    }
</script>
</head>
<body>
    <div id="chart_div" style="width:400px; height:120px;"></div>
    <image src="download_image.jpg" style="width:0px;height:0px;">
    Speed Test
</body>
<html>
""" % current_speed

        # Make bandwidth calculator
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()

        self.wfile.write(html)

        return


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-p", "--port", dest="port", help="TCP Port (default:80)")

    (options,args) = parser.parse_args()
    if not options.port:
        port = 80
    else:
        port = int(options.port)

    # Create Instance
    server = HTTPServer(('',port), myHandler)
    print 'Start HTTP server on port ', port
    server.serve_forever()
