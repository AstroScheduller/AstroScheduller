from .utilities import utilities


class schedule_edit():
    def __init__(self):
        '''
        Initialize a schedule object.
        '''

        self.u = utilities()
        self.a = 1

    def item(self, **kwargs):
        '''
        Get an item from the schedule.
        Provide one or more of the following arguments:
        - identifier: The identifier of the item.
        - index: The index of the item.
        - ra: The right ascension of the item.
        - dec: The declination of the item.
        - duration: The duration of the item.
        - weight: The weight of the item.
        - important: Is the item important?

        Return:
        The item.
        If more than one object is found, exception will be raised.
        '''

        itemKeys = ["identifier", "ra", "dec", "duration", "weight", "important", "index"]

        for kwargsKey in kwargs:
            if(kwargsKey not in itemKeys):
                raise Exception("itemKey", kwargsKey)

        gradedItems = list()
        for i in range(len(self.objects_all())):
            thisGrade = 0
            thisObj = self.objects_all()[i]
            for thisKey in kwargs:
                if(thisKey == "index"):
                    if(i == (kwargs[thisKey] - 1)):
                        thisGrade += 1
                elif(self.u.str_format(kwargs[thisKey]) == self.u.str_format(thisObj[thisKey])):
                    thisGrade += 1

            gradedItems.append({"index": i, "grade": thisGrade})
        
        gradedItems.sort(key=lambda x: x["grade"], reverse=True)

        findedItem = list()
        for gradedItem in gradedItems:
            if(gradedItem["grade"] != len(kwargs)):
                break
            findedItem.append(gradedItem["index"])
        
        if(len(findedItem) == 1):
            return item_operation(self, findedItem[0])
        elif(len(findedItem) > 1):
            raise Exception("item", findedItem, "more than one item has been founded.")
        else:
            raise Exception("item", findedItem, "item not found.")
    
    def append(self, item):
        '''
        Append an item to the schedule.
        '''

        self.objects.append(item.get_object())
    
    def insert(self, item, index):
        '''
        Insert an item to the schedule.
        '''

        self.objects.insert(index, item.get_object())

class item_operation():
    def __init__(self, self_upper, index):
        '''
        Initialize an item object.
        '''

        self.self_upper = self_upper
        self.index = index

    def __str__(self):
        '''
        Get the string of the item.
        '''

        return str(self.self_upper.objects_all()[self.index])
    
    def __repr__(self):
        '''
        Get the representation of the item.
        '''

        return str(self.self_upper.objects_all()[self.index])
    
    def wait(self, waitTime):
        '''
        Get the wait time of the object in seconds.
        '''

        self.self_upper.objects[self.index]["wait"] = waitTime

    def get_index(self):
        '''
        Get the index of the item.
        '''

        return self.index
    
    def get_object(self):
        '''
        Get the object of the item.
        '''

        return self.self_upper.objects_all()[self.index]

    def move_forward(self, step = 1):
        '''
        Move the item forward.
        step: The step to move forward.
        '''

        thisObj = self.self_upper.objects_all()[self.index]
        nextObj = self.self_upper.objects_all()[self.index + step]
        
        self.self_upper.objects[self.index] = nextObj
        self.self_upper.objects[self.index + step] = thisObj

        self.index = self.index + step

    def move_backward(self, step = 1):
        '''
        Move the item backward.
        step: The step to move backward.
        '''
        thisObj = self.self_upper.objects_all()[self.index]
        prevObj = self.self_upper.objects_all()[self.index - step]
        
        self.self_upper.objects[self.index] = prevObj
        self.self_upper.objects[self.index - step] = thisObj

        self.index = self.index - step

    def assign_before(self, item):
        '''
        Assign the item before the item.
        item: to assign before this item.
        '''

        itemIndex = item.get_index()
        thisObj = self.self_upper.objects_all()[self.index]

        if(itemIndex == self.index):
            raise("item", item, "is the same as", thisObj)

        self.self_upper.objects.insert(itemIndex, thisObj)

        if(self.index > itemIndex):
            del self.self_upper.objects[self.index + 1]
        else:
            del self.self_upper.objects[self.index]
        
        self.index = itemIndex

    def assign_after(self, item):
        '''
        Assign the item after the item.
        item: to assign after this item.
        '''

        itemIndex = item.get_index() + 1
        thisObj = self.self_upper.objects_all()[self.index]

        if(itemIndex == self.index):
            raise("item", item, "is the same as", thisObj)

        self.self_upper.objects.insert(itemIndex, thisObj)

        if(self.index > itemIndex):
            del self.self_upper.objects[self.index + 1]
        else:
            del self.self_upper.objects[self.index]

        self.index = itemIndex

    def to_begin(self):
        '''
        Move the item to the begin of the schedule.
        '''
        
        thisObj = self.self_upper.objects_all()[self.index]

        del self.self_upper.objects[self.index]
        self.self_upper.objects.insert(0, thisObj)

        self.index = 0

    def to_end(self):
        '''
        Move the item to the end of the schedule.
        '''
        
        thisObj = self.self_upper.objects_all()[self.index]

        del self.self_upper.objects[self.index]
        self.self_upper.objects.append(thisObj)

        self.index = len(self.self_upper.objects) - 1

    def remove(self):
        '''
        Remove the item from the schedule.
        '''
        
        del self.self_upper.objects[self.index]

        self.index = -1