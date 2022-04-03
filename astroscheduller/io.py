import json
import pickle

from sympy import true
from .utilities import utilities
from xml.dom import minidom

class schedule_from():
    def from_xml(self, xmlString):
        if(utilities().is_file(xmlString)):
            xmlString = open(xmlString, "r+").read()

        xml = minidom.parseString(xmlString)
        node = xml.getElementsByTagName("scheduller")

        # Observation
        observation = node[0].getElementsByTagName("observation")

        ## Duration
        duration = observation[0].getElementsByTagName("duration")
        ### Begin & End
        durationBegin = duration[0].getElementsByTagName("begin")
        durationEnd = duration[0].getElementsByTagName("end")
        ### Set Duration
        self.set_duration(
            begin = durationBegin[0].childNodes[0].nodeValue, 
            end = durationEnd[0].childNodes[0].nodeValue, 
            format = "timestamp"
        )
        
        ## Telescope
        telescope = observation[0].getElementsByTagName("telescope")
        ### Latitude
        telescopeLatitude = telescope[0].getElementsByTagName("latitude")
        ### Longitude
        telescopeLongitude = telescope[0].getElementsByTagName("longitude")
        ### Altitude
        telescopeAltitude = telescope[0].getElementsByTagName("altitude")
        ### Velocity
        telescopeVelocity = telescope[0].getElementsByTagName("velocity")
        #### Ra & Dec
        telescopeVelocityRa = telescopeVelocity[0].getElementsByTagName("ra")
        telescopeVelocityDec = telescopeVelocity[0].getElementsByTagName("dec")
        ### Set Telescope
        self.set_telescope(
            latitude = telescopeLatitude[0].childNodes[0].nodeValue,
            longitude = telescopeLongitude[0].childNodes[0].nodeValue,
            altitude =  telescopeAltitude[0].childNodes[0].nodeValue,
            velocity = [
                telescopeVelocityRa[0].childNodes[0].nodeValue,
                telescopeVelocityDec[0].childNodes[0].nodeValue
            ]
        )

        ## Elevation
        elevation = observation[0].getElementsByTagName("elevation")
        ### Minimal
        elevationMinimal = elevation[0].getElementsByTagName("minimal")
        ### Maximal
        elevationmaximal = elevation[0].getElementsByTagName("maximal")
        ### Set Elevation
        self.set_elevation(
            minimal = elevationMinimal[0].childNodes[0].nodeValue,
            maximal = elevationmaximal[0].childNodes[0].nodeValue
        )

        ## Escape
        escape = observation[0].getElementsByTagName("escape")
        ### Sun
        escapeSun = escape[0].getElementsByTagName("sun")
        ### Set Escape
        self.set_escape(
            sun = escapeSun[0].childNodes[0].nodeValue
        )

        # Sources
        sources = node[0].getElementsByTagName("sources")
        ## Objects
        lastObjectEnded = self.observation["duration"]["begin"]
        objects = sources[0].getElementsByTagName("object")
        for thisObj in objects:
            ### Identifier
            identifier = thisObj.getElementsByTagName("identifier")
            ### Ra
            ra = thisObj.getElementsByTagName("ra")
            ### Dec
            dec = thisObj.getElementsByTagName("dec")
            ### Duration
            duration = thisObj.getElementsByTagName("duration")

            ### Weight
            weightNode = thisObj.getElementsByTagName("weight")
            try:
                weight = weightNode[0].childNodes[0].nodeValue
            except Exception as e:
                weight = 1

            ### Important
            importantNode = thisObj.getElementsByTagName("important")
            try:
                important = importantNode[0].childNodes[0].nodeValue
            except Exception as e:
                important = 0

            ### Schedule Wait
            wait = 0
            ScheduleNode = thisObj.getElementsByTagName("Schedule")
            try:
                DurationsNode = ScheduleNode[0].getElementsByTagName("Duration")
                Duration = [int(DurationsNode[0].childNodes[0].nodeValue), int(DurationsNode[1].childNodes[0].nodeValue)]
                wait = Duration[0] - lastObjectEnded
                
                lastObjectEnded = Duration[1]
            except Exception as e:
                pass
            
            ### Add Object
            self.add_object(
                identifier = identifier[0].childNodes[0].nodeValue,
                ra = ra[0].childNodes[0].nodeValue,
                dec = dec[0].childNodes[0].nodeValue,
                duration = duration[0].childNodes[0].nodeValue,
                weight = weight, 
                important = important, 
                wait = wait
            )

class schedule_to():
    def to_dict(self, filename = False):
        if(filename != False):
            return self.to_json(filename)

        return {
            "observation": self.observation, 
            "object": self.objects
        }
    
    def to_json(self, filename = False):
        if(filename != False):
            return open(filename, "w+").write(json.dumps(self.to_dict()))

        return json.dumps(self.to_dict())

    def to_xml(self, filename = False):
        xmlHandle = minidom.Document() 
        
        # Observation
        observation = xmlHandle.createElement("observation")

        ## Duration
        duration = xmlHandle.createElement("duration")
        ### Begin
        durationBegin = xmlHandle.createElement("begin")
        durationBegin.appendChild(xmlHandle.createTextNode(str(self.observation["duration"]["begin"])))
        duration.appendChild(durationBegin)
        ### End
        durationEnd = xmlHandle.createElement("end")
        durationEnd.appendChild(xmlHandle.createTextNode(str(self.observation["duration"]["end"])))
        duration.appendChild(durationEnd)

        ## Telescope
        telescope = xmlHandle.createElement("telescope")
        ### Latitude
        telescopeLatitude = xmlHandle.createElement("latitude")
        telescopeLatitude.appendChild(xmlHandle.createTextNode(str(self.observation["telescope"]["latitude"])))
        telescope.appendChild(telescopeLatitude)
        ### Longitude
        telescopeLongitude = xmlHandle.createElement("longitude")
        telescopeLongitude.appendChild(xmlHandle.createTextNode(str(self.observation["telescope"]["longitude"])))
        telescope.appendChild(telescopeLongitude)
        ### Altitude
        telescopeAltitude = xmlHandle.createElement("altitude")
        telescopeAltitude.appendChild(xmlHandle.createTextNode(str(self.observation["telescope"]["altitude"])))
        telescope.appendChild(telescopeAltitude)
        ### Velocity
        telescopeVelocity = xmlHandle.createElement("velocity")
        #### Ra
        telescopeVelocityRa = xmlHandle.createElement("ra")
        telescopeVelocityRa.appendChild(xmlHandle.createTextNode(str(self.observation["telescope"]["velocity"]["ra"])))
        telescopeVelocity.appendChild(telescopeVelocityRa)
        #### Dec
        telescopeVelocityDec = xmlHandle.createElement("dec")
        telescopeVelocityDec.appendChild(xmlHandle.createTextNode(str(self.observation["telescope"]["velocity"]["dec"])))
        telescopeVelocity.appendChild(telescopeVelocityDec)
        telescope.appendChild(telescopeVelocity)

        ## Elevation
        elevation = xmlHandle.createElement("elevation")
        ### Minimal
        elevationMinimal = xmlHandle.createElement("minimal")
        elevationMinimal.appendChild(xmlHandle.createTextNode(str(self.observation["elevation"]["minimal"])))
        elevation.appendChild(elevationMinimal)
        ### Maximal
        elevationMaximal = xmlHandle.createElement("maximal")
        elevationMaximal.appendChild(xmlHandle.createTextNode(str(self.observation["elevation"]["maximal"])))
        elevation.appendChild(elevationMaximal)

        ## Escape
        escape = xmlHandle.createElement("escape")
        ### Minimal
        escapeSun = xmlHandle.createElement("sun")
        escapeSun.appendChild(xmlHandle.createTextNode(str(self.observation["escape"]["sun"])))
        escape.appendChild(escapeSun)
        
        observation.appendChild(duration)
        observation.appendChild(telescope)
        observation.appendChild(elevation)
        observation.appendChild(escape)

        # Objects
        sources = xmlHandle.createElement("sources")
        
        ## Append Objects
        for thisObj in self.objects:
            object = xmlHandle.createElement("object")
            
            ### Identifier
            identifier = xmlHandle.createElement("identifier")
            identifier.appendChild(xmlHandle.createTextNode(str(thisObj['identifier'])))
            object.appendChild(identifier)

            ### Ra
            ra = xmlHandle.createElement("ra")
            ra.appendChild(xmlHandle.createTextNode(str(thisObj['ra'])))
            object.appendChild(ra)

            ### Dec
            dec = xmlHandle.createElement("dec")
            dec.appendChild(xmlHandle.createTextNode(str(thisObj['dec'])))
            object.appendChild(dec)

            ### Duration
            duration = xmlHandle.createElement("duration")
            duration.appendChild(xmlHandle.createTextNode(str(thisObj['duration'])))
            object.appendChild(duration)

            ### Weight
            weight = xmlHandle.createElement("weight")
            weight.appendChild(xmlHandle.createTextNode(str(thisObj['weight'])))
            object.appendChild(weight)

            ### Important
            important = xmlHandle.createElement("important")
            important.appendChild(xmlHandle.createTextNode(str(thisObj['important'])))
            object.appendChild(important)

            sources.appendChild(object)

        xml = xmlHandle.createElement("scheduller")
        xml.appendChild(observation)
        xml.appendChild(sources)

        if(filename != False):
            return open(filename, "w+").write(xml.toprettyxml())

        return xml.toprettyxml()
    
    def to_csv(self, filename = False):
        csv = ""
        csv += "Identifier, R.A., Dec., Duration, Weight, Important, Wait\n"
        for thisObj in self.objects:
            csv += str(thisObj["identifier"]) + ", "
            csv += str(thisObj["ra"]) + ", "
            csv += str(thisObj["dec"]) + ", "
            csv += str(thisObj["duration"]) + ", "
            csv += str(thisObj["weight"]) + ", "
            csv += str(thisObj["important"]) + ", "
            csv += str(thisObj["wait"]) + "\n"
        
        '''
        csv += " , , , , , , , \n"
        csv += "Additional Information, , , , , , , \n"
        csv += "Observation, " + "Timestamp: " + str(self.observation["duration"]["begin"] )+ " - " + str(self.observation["duration"]["end"]) + "\n"
        csv += "Tele. Loca., " + "Latitude: " + str(self.observation["telescope"]["latitude"]) + ", " + "Longitude: " + str(self.observation["telescope"]["longitude"]) + ", " + "Altitude: "  + str(self.observation["telescope"]["altitude"]) + "\n"
        csv += "Tele. Elev., " + str(self.observation["elevation"]["minimal"]) + " - " + str(self.observation["elevation"]["maximal"]) + " Deg. \n"
        csv += "Tele. Escp, " + str(self.observation["escape"]["sun"]) + " Deg. \n"
        csv += "Object Number, " + str(len(self.objects)) + "\n"
        '''
        
        if(filename != False):
            return open(filename, "w+").write(csv)

        return csv
    
    def to_table(self, filename = False):
        table = ""
        table += "| Identifier | RA | Dec | Duration | Weight | Important |\n"
        table += "| --- | --- | --- | --- | --- | --- |\n"
        for thisObj in self.objects:
            table += "| " + thisObj["identifier"] + " | "
            table += str(thisObj["ra"]) + " | "
            table += str(thisObj["dec"]) + " | "
            table += str(thisObj["duration"]) + " | "
            table += str(thisObj["weight"]) + " | "
            table += str(thisObj["important"]) + " |\n"
        
        if(filename != False):
            return open(filename, "w+").write(table)

        return table
    
    def to_html(self, filename = False):
        html = ""
        html += "<table>\n"
        html += "<tr>\n"
        html += "<th>Identifier</th>\n"
        html += "<th>RA</th>\n"
        html += "<th>Dec</th>\n"
        html += "<th>Duration</th>\n"
        html += "<th>Weight</th>\n"
        html += "<th>Important</th>\n"
        html += "</tr>\n"
        for thisObj in self.objects:
            html += "<tr>\n"
            html += "<td>" + thisObj["identifier"] + "</td>\n"
            html += "<td>" + str(thisObj["ra"]) + "</td>\n"
            html += "<td>" + str(thisObj["dec"]) + "</td>\n"
            html += "<td>" + str(thisObj["duration"]) + "</td>\n"
            html += "<td>" + str(thisObj["weight"]) + "</td>\n"
            html += "<td>" + str(thisObj["important"]) + "</td>\n"
            html += "</tr>\n"
        html += "</table>\n"

        if(filename != False):
            return open(filename, "w+").write(html)

        return html

    def to_latex(self, filename = False):
        latex = ""
        latex += "\\begin{table}\n"
        latex += "\\begin{tabular}{|l|l|l|l|l|l|}\n"
        latex += "\\hline\n"
        latex += "Identifier & RA & Dec & Duration & Weight & Important \\\\ \\hline\n"
        for thisObj in self.objects:
            latex += thisObj["identifier"] + " & "
            latex += str(thisObj["ra"]) + " & "
            latex += str(thisObj["dec"]) + " & "
            latex += str(thisObj["duration"]) + " & "
            latex += str(thisObj["weight"]) + " & "
            latex += str(thisObj["important"]) + " \\\\ \\hline\n"
        latex += "\\end{tabular}\n"
        latex += "\\end{table}\n"

        if(filename != False):
            return open(filename, "w+").write(latex)

        return latex

class scheduller_io():
    def save(self, filename):
        # Check if filename has .ash extension
        if(filename[-4:] != ".ash"):
            filename += ".ash"

        ashSession = {
            "objects": {
                "observation": self.objects.observation,
                "objects": self.objects.objects
            }, 
            "schedule": {
                "observation": self.schedule.observation,
                "objects": self.schedule.objects
            }
        }

        with open(filename, 'wb') as outfile:
            pickle.dump(ashSession, outfile)

        return filename
    
    def load(self, filename):
        with open(filename, 'rb') as infile:
            ashSession = pickle.load(infile)

        self.objects.observation = ashSession["objects"]["observation"]
        self.objects.objects = ashSession["objects"]["objects"]
        self.schedule.observation = ashSession["schedule"]["observation"]
        self.schedule.objects = ashSession["schedule"]["objects"]

        return True
    
    def open(self, filename):
        return self.load(filename)