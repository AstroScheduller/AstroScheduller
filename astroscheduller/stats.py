import copy

class scheduller_stats():
    def objects_all(self):
        '''
        Return all objects.
        
        return: list of objects.
        '''

        return self.objects.objects_all()
    
    def objects_scheduled(self):
        '''
        Return scheduled objects.
        
        return: list of objects.
        '''
        
        return self.schedule.objects_all()

    def objects_unscheduled(self):
        '''
        Return unscheduled objects.

        return: list of objects.
        '''

        objectsUnscheduled = copy.deepcopy(self.objects_all())

        for thisObj in self.objects_scheduled():
            for i in range(len(objectsUnscheduled)):
                if(thisObj["identifier"] == objectsUnscheduled[i]["identifier"]):
                    del objectsUnscheduled[i]
                    break
        
        return objectsUnscheduled

    def num_all(self):
        '''
        Return the number of all objects.
        
        return: number of all objects.
        '''

        return len(self.objects_all())

    def num_all_objects(self):
        '''
        Return the number of all objects. As a shortcut.
        
        return: number of all objects.
        '''
        return self.num_all()

    def num_scheduled(self):
        '''
        Return the number of scheduled objects.
        
        return: number of scheduled objects.
        '''
        
        return len(self.objects_scheduled())

    def num_scheduled_objects(self):
        '''
        Return the number of scheduled objects. As a shortcut.
        
        return: number of scheduled objects.
        '''
        
        return self.num_scheduled()

    def num_unscheduled(self):
        '''
        Return the number of unscheduled objects.
        
        return: number of unscheduled objects.
        '''
        
        return len(self.objects_unscheduled())

    def num_unscheduled_objects(self):
        '''
        Return the number of unscheduled objects. As a shortcut.
        
        return: number of unscheduled objects.
        '''
        
        return self.num_unscheduled()

    def len_observation(self):
        '''
        Return the length of observation.
        
        return: length of observation.
        '''
        
        duration = 0

        for thisObj in self.objects_scheduled():
            duration = duration + thisObj["duration"]
        
        return duration
    
    def len_wait(self):
        '''
        Return the length of wait time.
        
        return: length of wait time.
        '''
        
        wait = 0

        for thisObj in self.objects_scheduled():
            wait = wait + thisObj["wait"]
        
        return wait
    
    def ids_objects(self):
        '''
        Return the list of all object identifiers.
        '''
        
        ids = list()

        for thisObj in self.objects_all():
            ids.append(thisObj["identifier"])
        
        return ids

    def ids_scheduled(self):
        '''
        Return the list of scheduled object identifiers.
        
        return: list of object identifiers.
        '''
        
        ids = list()

        for thisObj in self.objects_scheduled():
            ids.append(thisObj["identifier"])
        
        return ids

    def ids_scheduled_objects(self):
        '''
        Return the list of scheduled object identifiers. As a shortcut.

        return: list of object identifiers.
        '''
        
        return self.ids_scheduled
    
    def ids_unscheduled(self):
        '''
        Return the list of unscheduled object identifiers.
        
        return: list of object identifiers.
        '''
        
        ids = list()

        for thisObj in self.objects_unscheduled():
            ids.append(thisObj["identifier"])
        
        return ids
    
    def ids_unscheduled_objects(self):
        '''
        Return the list of unscheduled object identifiers. As a shortcut.
        
        return: list of object identifiers.
        '''
        
        return self.objects_unscheduled()
        
    def rate_schedule(self):
        '''
        Return the schedule rate.
        
        return: schedule rate.
        '''
        
        return (self.num_scheduled() / self.num_all())

    def stats(self):
        '''
        Print the schedule statistics.
        '''
        print("========== STATS ==========")
        print("| All Objects:", self.num_all())
        print("| Scheduled Objects:", self.num_scheduled())
        print("| Unscheduled Objects:", self.num_unscheduled())
        print("| Observation Duration:", self.len_observation())
        print("| Wait Duration:", self.len_wait())
        print("| Schedule Rate:", '{:.2%}'.format(self.rate_schedule()))
        print("===========================")

class schedule_stats():
    def objects_all(self):
        '''
        Return all objects.
        
        return: list of objects.
        '''
        
        return self.objects

    def num_objects(self):
        '''
        Return the number of objects.
        
        return: number of objects.
        '''
        
        return len(self.objects_all())

    def num_all_objects(self):
        '''
        Return the number of all objects. As a shortcut.
        
        return: number of all objects.
        '''
        
        return self.num_objects()

    def len_observation(self):
        '''
        Return the length of observation.
        
        return: length of observation.
        '''
        
        duration = 0

        for thisObj in self.objects_scheduled():
            duration = duration + thisObj["duration"]
        
        return duration
    
    def ids_objects(self):
        '''
        Return the list of all object identifiers.
        
        return: list of object identifiers.
        '''
        
        ids = list()

        for thisObj in self.objects_all():
            ids.append(thisObj["identifier"])
        
        return ids