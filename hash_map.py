class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None
        self.kvpair= (key, value)


class hashmap:
    def __init__(self):
        self.capacity= 50
        self.size = 0
        self.buckets = [None]*self.capacity

    def insert(self,key, value):
        index = key % self.capacity
        if self.buckets[index] is None:
            self.buckets[index] = Node(key, value)
        else:
            current = self.buckets[index]
            while current.next is not None:
                if current.kvpair[0] == key:
                    current.kvpair = (key, value) # update value if key already exists
                    return
                current = current.next
            current.next = Node(key, value)
    def lookup(self, key):
        index = key % self.capacity
        if self.buckets[index] is None:
            return None
        else:
            current = self.buckets[index]
            while current is not None:
                if current.kvpair[0] == key:
                    return current.kvpair[1] # return value if key exists
                else:
                    current = current.next
            return None

    def remove(self, key):
        index = key % self.capacity
        if self.buckets[index] is None:
            return
        elif self.buckets[index].kvpair[0] == key:
            self.buckets[index] = self.buckets[index].next
        else:
            current = self.buckets[index]
            while current.next is not None:
                if current.next.kvpair[0] == key:
                    current.next = current.next.next
                    return
                current = current.next

