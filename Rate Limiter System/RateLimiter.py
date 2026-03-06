import threading
from collections import deque
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, n, t):
        self.N = n
        self.T = t
        self.user_requests = {}
        self._lock = threading.RLock()
    
    def allow_request(self, user_id):
        with self._lock:            
            if user_id not in self.user_requests:
                self.user_requests[user_id] = deque()
            reqs = self.user_requests[user_id]
            now = datetime.now()
            oldest = now - timedelta(seconds=self.T)
            
            while reqs and reqs[0] < oldest:
                reqs.popleft()
                
            if len(reqs) < self.N:
                reqs.append(now)
                return True
            
            return False
        

if __name__=='__main__':
    rateLimiter = RateLimiter(3, 10)
    print(rateLimiter.allow_request("u1"))
    print(rateLimiter.allow_request("u2"))
    print(rateLimiter.allow_request("u1"))
    print(rateLimiter.allow_request("u3"))
    print(rateLimiter.allow_request("u1"))
    print(rateLimiter.allow_request("u1"))
    print(rateLimiter.allow_request("u1"))
    print(rateLimiter.allow_request("u2"))
    print(rateLimiter.allow_request("u4"))
