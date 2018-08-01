#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import webapp2, jinja2, os, json, urllib

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render())

class GlobeHandler(webapp2.RequestHandler):
    JSON_URL = "https://data.nasa.gov/resource/y77d-th95.json"
    globe_data = ["Meteorites", []] # Expected data format for Globe

    response = urllib.urlopen(JSON_URL)
    json_data = json.loads(response.read())

    def default_filter(self):
        for entry in self.json_data:
            if "reclat" in entry and "reclong" in entry and "mass" in entry:
                lat = entry["reclat"]
                long = entry["reclong"]
                mag = float(entry["mass"])*0.00001
            else:
                continue

            self.globe_data[1].extend((lat, long, mag))

    def post(self):
        filter = self.request.get("filter")
        if filter == "default":
            self.default_filter()

        template = jinja_environment.get_template('globe.html')
        self.response.out.write(template.render(globe_data=json.dumps(self.globe_data)))

app = webapp2.WSGIApplication(
    [('/', MainHandler),
    ('/globe', GlobeHandler)],
    debug=True)
