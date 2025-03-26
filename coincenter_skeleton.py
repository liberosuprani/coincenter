import pickle, struct
from coincenter_data import *

class CoincenterSkeleton:
    def __init__(self):
        self.response = []

    def process_request(self, request) -> tuple[int, list]:
        try:
            request = pickle.loads(request)
            print(f"RECV: {request}") 

            self.response = ClientController.process_request(request)

            bytes_response = pickle.dumps(self.response)
            bytes_response_size = struct.pack("i", len(bytes_response))

            print(f"SENT: {self.response}") 
        except:
            return (0, [])
        
        return (bytes_response_size, bytes_response)
