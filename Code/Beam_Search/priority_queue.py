import Code.Beam_Search.constraints as cs

class PriorityQueue:
    
    def __init__(self, max_length: int, queue=[]):
        self.queue = queue #Form [(desc, quality, idx_sg), (desc, quality, idx_sg), ...]
        self.max_length = max_length
 
    def __str__(self):
        return ' '.join([str(i, qm) for i, qm, _ in self.queue])
 
    def insert(self, element):
        
        """ 
        Insert an element in the queue.
        Check whether the priority queue is not full.
        Otherwise, check if the element is of higher quality
        than the worst element. 
        """
        
        #First, check for redundancy in the priority queue
        if len(self.queue) > 0:
            redundancy_found, best_descr, idx_descr = cs.remove_redundant_descriptions(self.queue, element)
            
            if redundancy_found:
                if best_descr == 'new_desc':
                    self.queue[idx_descr] = element
                    
                elif best_descr == 'old_desc':
                    #Nothing changes
                    self.queue = self.queue
                    
                else:
                    print('Something went wrong.')
            
            else:
                if len(self.queue) < self.max_length:
                    self.queue.append(element)
                    self.queue = sorted(self.queue, reverse=True, key = lambda i: i[1])
        
                else:
                    if element[1] > self.queue[-1][1]: #No improvement on existing, even though quality might be the same
                        self.queue.pop(-1)
                        self.queue.append(element)
                        self.queue = sorted(self.queue, reverse=True, key = lambda i: i[1])
                    else:
                        self.queue = self.queue #Nothing happens and it is already sorted
        else:
            self.queue.append(element)
    
    def get_descriptions(self):
        return [descr for descr, _, _ in self.queue]
    
    def get_qualities(self):
        return [quality for _, quality, _ in self.queue]
    
    def get_idx(self):
        return [idx_sg for _, _, idx_sg in self.queue]
    
    def get_queue(self):
        return self.queue
    
            
 

