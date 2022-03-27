from utilities import utilities


class schedule_edit():
    def __init__(self):
        self.u = utilities()
        self.a = 1

    def item(self, **kwargs):
        itemKeys = ["identifier", "ra", "dec", "duration", "weight", "important"]

        for kwargsKey in kwargs:
            if(kwargsKey not in itemKeys):
                raise Exception("itemKey", kwargsKey)

        findedItem = list()
        for i in range(len(self.objects_all())):
            thisObj = self.objects_all()[i]
            for thisKey in kwargs:
                if(self.u.str_format(kwargs[thisKey]) == self.u.str_format(thisObj[thisKey])):
                    findedItem.append(i)
        
        if(len(findedItem) == 1):
            return item_operation(self, findedItem[0])
        else:
            raise Exception("item", findedItem, "not found or more than one")
    
    def append(self, item):
        self.objects.append(item.get_object())
    
    def insert(self, item, index):
        self.objects.insert(index, item.get_object())

class item_operation():
    def __init__(self, self_upper, index):
        self.self_upper = self_upper
        self.index = index
    
    def wait(self, waitTime):
        self.self_upper.objects[self.index]["wait"] = waitTime

    def get_index(self):
        return self.index
    
    def get_object(self):
        return self.self_upper.objects_all()[self.index]

    def move_forward(self, step = 1):
        thisObj = self.self_upper.objects_all()[self.index]
        nextObj = self.self_upper.objects_all()[self.index + step]
        
        self.self_upper.objects[self.index] = nextObj
        self.self_upper.objects[self.index + step] = thisObj

        self.index = self.index + step

    def move_backward(self, step = 1):
        thisObj = self.self_upper.objects_all()[self.index]
        prevObj = self.self_upper.objects_all()[self.index - step]
        
        self.self_upper.objects[self.index] = prevObj
        self.self_upper.objects[self.index - step] = thisObj

        self.index = self.index - step

    def assign_before(self, item):
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
        thisObj = self.self_upper.objects_all()[self.index]

        del self.self_upper.objects[self.index]
        self.self_upper.objects.insert(0, thisObj)

        self.index = 0

    def to_end(self):
        thisObj = self.self_upper.objects_all()[self.index]

        del self.self_upper.objects[self.index]
        self.self_upper.objects.append(thisObj)

        self.index = len(self.self_upper.objects) - 1

    def remove(self):
        del self.self_upper.objects[self.index]

        self.index = -1