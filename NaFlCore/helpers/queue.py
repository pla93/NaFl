#
# Queues and stuff
#

from Queue import PriorityQueue
from minimization_utils import sub_queue_min


mutationQueue = PriorityQueue()
processedQueue = PriorityQueue()


class FileToMutate(object):
    """
    This is a convenient object.
    Example:
    q = Queue.PriorityQueue()
    q.put(FileToMutate(1, 'c:\\tests\\file.123.txt'))
    """
    def __init__(self, priority, filename, id, bitmap):
        self.priority = priority
        self.filename = filename
        self.id = id
        self.bitmap = bitmap
        self.descendants = []

    def new_descendant(self, d):
        self.descendants.append(d)

    def __cmp__(self, other):
        return cmp(self.priority, other.priority)

    def __eq__(self, other):
        return self.id == other.id


def get_queue_element_by_id(id, q):
    """
    The function name is its own documentation :)
    """
    for e in q.queue:
        if e.id == id:
            return e

    return None


# def get_parent_by_id(id, q):
#     for e in q.queue:
#         print e.id
#         print e.descendants
#         if id in [f.id for f in e.descendants]:
#             return e.id
#     return None


def clean_queues():
    global mutationQueue
    global processedQueue

    new_m_queue = {}
    for q in [mutationQueue, processedQueue]:
        for f2m in q.queue:
            if f2m.bitmap is None:
                sub_queue = []
                des = f2m.descendants

                while 1:
                    new_files = []
                    if len(des) == 0:
                        break

                    for d in des:
                        sub_queue.append(d)
                        if len(d.descendants) > 0:
                            new_files.extend(d.descendants)
                    des = new_files

                if sub_queue:
                    min_set = sub_queue_min(*sub_queue)
                else:
                    min_set = []
                new_m_queue[file] = min_set

    while not mutationQueue.empty():
        mutationQueue.get_nowait()

    while not processedQueue.empty():
        processedQueue.get_nowait()

    for parent, children in new_m_queue.items():
        parent.descendants = []
        parent.descendants.extend(children)
        for c in children:
            c.descendants = []
            c.priority = 0
            mutationQueue.put(c)
        mutationQueue.put(parent)




