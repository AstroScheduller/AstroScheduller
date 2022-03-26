import json
from xml.dom import minidom

class schedule_from():
    def from_xml(self, xmlString):
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

            ### Schedule Gap
            gap = 0
            ScheduleNode = thisObj.getElementsByTagName("Schedule")
            try:
                GapNode = ScheduleNode[0].getElementsByTagName("Gap")
                gap = GapNode[0].childNodes[0].nodeValue
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
                wait = gap
            )

class schedule_to():
    def to_dict(self):
        return {
            "observation": self.observation, 
            "object": self.objects
        }
    
    def to_json(self):
        return json.dumps(self.to_dict())

    def to_xml(self):
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

        return xml.toprettyxml()