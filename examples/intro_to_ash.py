import astroscheduller as ash                                # Import AstroScheduller

# Prepare for an example
ash.example("https://raw.githubusercontent.com/xiawenke/AstroScheduller/Dev/tests/psr_list_debug.xml")

obsPlan = ash.scheduller()                                   # Create a new scheduller object
obsPlan.objects.from_xml("./example.xml")                    # Load the objects from a XML file
obsPlan.get_schedule()                                       # Generate the schedule
obsPlan.stats()                                              # Calculate the statistics
obsPlan.plot().show()                                        # Plot the schedule
obsPlan.schedule.to_table("./example.txt")                   # Export the schedule to a table