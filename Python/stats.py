import copy

class schedule_stats():
    def objects_all(self):
        return self.objects
    
    def objects_scheduled(self):
        return self.objectsScheduled

    def objects_unscheduled(self):
        objectsUnscheduled = copy.deepcopy(self.objects_all())

        for thisObj in self.objects_scheduled():
            for i in range(len(objectsUnscheduled)):
                if(thisObj["identifier"] == objectsUnscheduled[i]["identifier"]):
                    del objectsUnscheduled[i]
                    break
        
        return objectsUnscheduled

    def num_all(self):
        return len(self.objects_all())

    def num_all_objects(self):
        return self.num_all()

    def num_scheduled(self):
        return len(self.objects_scheduled())

    def num_scheduled_objects(self):
        return self.num_scheduled()

    def num_unscheduled(self):
        return len(self.objects_unscheduled())

    def num_unscheduled_objects(self):
        return self.num_unscheduled()

    def len_observation(self):
        duration = 0

        for thisObj in self.objects_scheduled():
            duration = duration + thisObj["duration"]
        
        return duration
    
    def ids_objects(self):
        ids = list()

        for thisObj in self.objects_all():
            ids.append(thisObj["identifier"])
        
        return ids

    def ids_scheduled(self):
        ids = list()

        for thisObj in self.objects_scheduled():
            ids.append(thisObj["identifier"])
        
        return ids

    def ids_scheduled(self):
        return self.ids_scheduled
    
    def ids_unscheduled(self):
        ids = list()

        for thisObj in self.objects_unscheduled():
            ids.append(thisObj["identifier"])
        
        return ids
    
    def ids_unscheduled_objects(self):
        return self.objects_unscheduled()
        
    def rate_schedule(self):
        return (self.num_scheduled() / self.num_all())

    def stats(self):
        print("========== STATS ==========")
        print("| All Objects:", self.num_all())
        print("| Scheduled Objects:", self.num_scheduled())
        print("| Unscheduled Objects:", self.num_unscheduled())
        print("| Schedule Rate:", '{:.2%}'.format(self.rate_schedule()))
        print("===========================")