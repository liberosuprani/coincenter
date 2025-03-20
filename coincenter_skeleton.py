import pickle
from coincenter_data import *

class CoincenterSkeleton:
    def __init__(self):
        self.response = []

    def process_request(self, request):
        try:
            request = pickle.loads(request)
            print(f"RECV: {request}") 

            self.response = ClientController.process_request(request)

            bytesResponse = pickle.dumps(self.response)
            print(f"SENT: {self.response}") 
        except:
            return []
        
        return bytesResponse
