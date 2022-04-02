import astroscheduller as ash


###############################
# Test core functions         #
###############################
ash.core().update()
ash.core().install("/Users/wenky/Documents/GitHub/AstroSchedullerGo/releases_latest/_scheduller_darwin_amd64.so")


###############################
# Test schObj functions       #
###############################
s = ash.schedule()
s.set_duration(begin = 1627110000, end = 1627196340, format = "timestamp")
s.set_telescope(latitude = 32.7015, longitude = -109.891284, altitude = 3185, velocity = [0.5, 0.6])
s.set_elevation(minimal = 30, maximal = 80)
s.set_escape(sun = 20)
s.add_object(
    identifier= "J0437–4715", 
    ra= "69.3167",
    dec= "-47.2527", 
    duration= "3555"
)
s.add_object(
    identifier= "J1012+5307", 
    ra= "153.13930897",
    dec= "53.11737904", 
    duration= "800", 
    weight= "0.2", 
    important= True
)


###############################
# Test scheduller functions   #
###############################
s1 = ash.scheduller()
s1.objects = s
s1.get_schedule()
s1.stats()


###############################
# Test IO functions           #
###############################
s4 = ash.scheduller()
objects = s4.objects
objects.from_xml(open("./tests/psr_list_debug_short.xml").read())
objects.from_xml(open("./tests/psr_list_long.xml").read())
s4.get_schedule()
schedule = s4.schedule
schedule.to_xml("./tests/xml_export.xml")
schedule.to_dict("./tests/dict_export.json")
schedule.to_json("./tests/json_export.json")
schedule.to_csv("./tests/csv_export.csv")
schedule.to_table("./tests/table_export.txt")
schedule.to_html("./tests/html_export.html")
schedule.to_latex("./tests/latex_export.tex")


###############################
# Test stats functions        #
###############################
s4.stats()

###############################
# Test plot functions         #
###############################
ashPlot = s4.plot()
ashPlot.show()
ashPlot.save("./tests/plot_export.pdf")

###############################
# Test edit functions         #
###############################
'''
print(s4.schedule.to_dict())
print(s4.schedule.item(identifier = "PSR J1012+5307").move_forward(1))
print(s4.schedule.to_dict())
print(s4.schedule.item(identifier = "PSR J1012+5307").move_backward(1))
print(s4.schedule.to_dict())
print(s4.schedule.item(identifier = "PSR J1012+5307").move_backward(2))
print(s4.schedule.to_dict())
print(s4.schedule.item(identifier = "PSR J1012+5307").assign_before(
    s4.schedule.item(identifier = "PSR B1541+09"),
))
print(s4.schedule.to_dict())
print(s4.schedule.item(identifier = "PSR J1012+5307").assign_after(
    s4.schedule.item(identifier = "PSR B1541+09"),
))
print(s4.schedule.to_dict())
print(s4.schedule.item(identifier = "PSR J1012+5307").to_begin())
print(s4.schedule.to_dict())
print(s4.schedule.item(identifier = "PSR J1012+5307").to_end())
print(s4.schedule.to_dict())
s4.schedule.append(
    s4.objects.item(identifier = "PSR J1012+5307")
)
print(s4.schedule.to_dict())
s4.schedule.insert(
    s4.objects.item(identifier = "PSR J1012+5307"), 
    3
)
print(s4.schedule.to_dict())
'''