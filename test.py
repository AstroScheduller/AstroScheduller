import sched
import astroscheduller as ash

################################
# Test core functions          #
################################
ash.core().update()
coreToInstall = "/Users/wenky/Documents/GitHub/AstroScheduller/releases_latest/_scheduller_darwin_amd64.so"
ash.core().install(coreToInstall)

if(open(coreToInstall, "rb").read() == open(ash.core().coreInfo["corePath"], "rb").read()):
    print("", "🟢Core is installed. 👌")
else:
    print("", "🔴Core is not installed. ❌")

print("🟢 ash.core: OK 👌")

################################
# Test schObj functions        #
################################
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
print("🟢 ash.schedule: OK 👌")

################################
# Test scheduller functions    #
################################
s1 = ash.scheduller()
s1.objects = s
s1.get_schedule()
s1.stats()
print("🟢 ash.scheduller: OK 👌")

################################
# Test Schedule IO functions   #
################################
s4 = ash.scheduller()
objects = s4.objects
objects.from_xml(open("./tests/psr_list_debug_short.xml").read())
# objects.from_xml(open("./tests/psr_list_long.xml").read())
s4.get_schedule()
schedule = s4.schedule
schedule.to_xml("./tests/xml_export.xml")
schedule.to_dict("./tests/dict_export.json")
schedule.to_json("./tests/json_export.json")
schedule.to_csv("./tests/csv_export.csv")
schedule.to_table("./tests/table_export.txt")
schedule.to_html("./tests/html_export.html")
schedule.to_latex("./tests/latex_export.tex")
schedule.to_defined("example.txt", "./tests/use_defined_export_example.txt")
schedule.to_defined("./tests/sched_format_definition.txt", "./tests/use_defined_export_example_sched.txt")
print("🟢 Schedule IO: OK 👌")


################################
# Test Scheduller IO functions #
################################
s5 = ash.scheduller()
s5.load(s4.save("./tests/scheduller_session"))
if(s5.objects.observation == s4.objects.observation and
   s5.objects.objects == s4.objects.objects and
   s5.schedule.observation == s4.schedule.observation and
   s5.schedule.objects == s4.schedule.objects):
    print("🟢 Scheduller IO: OK 👌")
else:
    print("🔴 Scheduller IO: Failed ❌")


################################
# Test stats functions         #
################################
s4.stats()
print("🟢 ash.stats: OK 👌")

################################
# Test plot functions          #
################################
ashPlot = s4.plot()
ashPlot.show()
ashPlot.save("./tests/plot_export.pdf")
print("🟢 ash.plot: OK 👌")

################################
# Test edit functions          #
################################
print(s4.schedule.to_dict())
print(s4.schedule.item(identifier = "PSR B0834+06", ra = 129.27350833, dec = 6.17071111, duration = 2400, weight = 1))
print(s4.schedule.item(identifier = "PSR B0834+06", ra = 129.27350833, dec = 6.17071111, duration = 2400, weight = 1, important = False))
print(s4.schedule.item(identifier = "PSR B0834+06", ra = 129.27350833, dec = 6.17071111, duration = 2400, weight = 1, important = 0))
print(s4.schedule.item(identifier = "PSR B0834+06", ra = 129.27350833, dec = 6.17071111, duration = 2400, weight = 1.0, important = False))
print(s4.schedule.item(identifier = "PSR B0834+06", ra = 129.27350833, dec = 6.17071111, duration = 2400.0, weight = 1.0, important = False))
print(s4.schedule.item(index = 1))
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
print("🟢 ash.edit: OK 👌")