from coincenter_data import *

class CoincenterSkeleton:
    def __init__(self):
        self.response = []

    def process_request(self, request) -> tuple[int, list]:
        try:
            print(request)
            if request[0] == USER_EXIT or request[0] == MGR_EXIT:
                self.response = [request[0]+1, True]
            else:
                self.response = ClientController.process_request(request)
            
            print(f"SENT: {self.response}") 
        except:
            return []
        
        return (self.response)
