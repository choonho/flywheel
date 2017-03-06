#!/usr/bin/env python

import os
import time
import urlparse

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from optparse import OptionParser

fp = open('2MB','rb')
output = fp.read()
fp.seek(0, os.SEEK_END)
volume =fp.tell()
fp.close()

current_speed = 0
history = []

class myHandler(BaseHTTPRequestHandler):
    # Handler for the GET requests
    def do_GET(self):
        print "GET: %s" % self.path
        o = urlparse.urlparse(self.path)
        req = o.path
        if req == "/":
            self.main_page()
        elif req == "/download_image.jpg":
            self.download_image(10)
        elif req == "/speed":
            self.send_speed()
        elif req == "/history":
            self.send_history()

        return

    def send_speed(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write("%s" % current_speed)
        return

    def send_history(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(','.join(map(str,history)))
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

        # Push to history
        global history
        history.append(current_speed)
        if len(history) > 60:
          history.pop(0)

        return


    def main_page(self):
        html = """<html>
<head>
<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
</head>
<body>
<table>
<tr>
<td>
    <div id="chart_div" style="width:400px; height:150px;"></div>
</td>
<td>
    <div id="curve_chart" style="width:600px; height:200px;"></div>
</td>
</tr>
<tr>
<td>
    <image src="download_image.jpg" style="width:0px;height:0px;">
  <button type="button" onclick="mytest = setInterval(do_test, 10000)">Start Speed Test</button>
  <button type="button" onclick="clearTimeout(mytest)">Stop Speed Test</button>
</td>
</tr>
</table>
</body>
<script type="text/javascript">
    google.charts.load('current', {'packages':['gauge','corechart']});
    google.charts.setOnLoadCallback(drawGauge);
    google.charts.setOnLoadCallback(drawLine);
    function drawGauge() {
        var data = google.visualization.arrayToDataTable([
            ['Label','Value'],
            ['Download',0]
            ]);
        var options = {
            width:400, height:120,
            redFrom:0, redTo:2,
            yellowFrom:2, yellowTo:4,
            max: 10 
            };
        var chart = new google.visualization.Gauge(document.getElementById('chart_div'));
        chart.draw(data, options);


        var current_speed = 0;
        setInterval(function() {
            console.log("call speed");
            var request = new XMLHttpRequest();
            request.open('GET','/speed', false);
            request.send(null);
            if (request.status == 200) {
              current_speed=parseFloat(request.responseText);
              if (current_speed > 100) {
                 options.max = 1000;
                 options.redFrom = 0;
                 options.redTo=200;
                 options.yellowFrom=200;
                 options.yellowTo=400;
              } else if (current_speed > 1000) {
                 options.max = 10000;
                 options.redFrom = 0;
                 options.redTo=2000;
                 options.yellowFrom=2000;
                 options.yellowTo=4000;
 
              } else {
                 options.max = 10;
                 options.redFrom = 0;
                 options.redTo=2;
                 options.yellowFrom=2;
                 options.yellowTo=4;
 
              }
              data.setValue(0, 1, request.responseText);
              chart.draw(data, options);
            }
            }, 5000);

       
    }

    function drawLine() {
        var options = {
          title: 'Download Bandwidth',
          curveType: 'function',
          vAxis: {title:'Mbps'},
          legend: { position: 'bottom' }
        };

        var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));


        setInterval(function() {
            console.log("call history");

            var request = new XMLHttpRequest();
            request.open('GET','/history', false);
            request.send(null);
            var data = new google.visualization.DataTable();
            data.addColumn('number','count');
            data.addColumn('number','bandwidth');
            if (request.status == 200) {
              result = request.responseText.split(",");
              for(var i in result) {
                console.log(i);
                console.log(result[i]);
                data.addRow([parseInt(i),parseFloat(result[i])]);
              }
              console.log(result);
              chart.draw(data, options);
            }
            delete request;
            delete data;
            }, 5000);



    }

    var count = 1;
    function do_test() {
      var img = new Image();
          console.log("download image");
          img.src = "/download_image.jpg?" + count;
          console.log(count);
          count = count + 1;
    }

</script>

<html>
""" 

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
