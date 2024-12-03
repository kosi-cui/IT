import requests

class Agent:
    def __init__(self, key=None, url=None):
        """
        Initializes the Agent object with the API key and URL of the helpdesk.
        """
        self.key = key
        self.url = url
        self.current_ticket = None
        self.filtered_ticket_list = None
        if self.url != None and self.key != None:
            self.valid_user = self.validKey()
        else:
            self.valid_user = False
        self.users = None
        self.getAllUsers()


    def validKey(self) -> bool:
        """
        Checks if the API key and URL are valid.
        """
        url = self.url + "/api/v2/tickets.json"
        response = requests.get(url, auth=(self.key, "X"))
        if response.status_code == 200:
            return True
        else:
            return False


    # Setters
    def setKey(self, key):
        self.key = key
        if self.url != None:
            self.valid_user = self.validKey()


    def setUrl(self, url):
        self.url = url
        if self.key != None:
            self.valid_user = self.validKey()


    # Decorators
    def authMethod(func):
        """
        Decorator to check if the user is valid before making a request.
        This function is used to decorate all the methods that require a valid user.
        """
        def wrapper(self, *args, **kwargs):
            if not self.valid_user:
                return None
            return func(self, *args, **kwargs)
        return wrapper


    def reqTicket(func):
        """
        Decorator to check if there is a current ticket before making a request.
        This function is used to decorate all the methods that require a current ticket.
        """
        def wrapper(self, *args, **kwargs):
            if self.current_ticket == None:
                return None
            return func(self, *args, **kwargs)
        return wrapper


    # Ticket Functions -- Requires valid API Key & URL
    @authMethod # Uses the authMethod decorator to check if the user is valid -- If not valid user, then the function will return None
    def ticketGetRequest(self, ticket_id):
        """
        Makes a GET request to the helpdesk API to get the ticket with the specified ID.
        Returns the ticket if it exists, otherwise returns an error message.
        Also updates the Agent's current_ticket attribute to the ticket that was just retrieved.
        """
        url = self.url + "/api/v2/tickets/" + str(ticket_id) + ".json"
        response = requests.get(url, auth=(self.key, "X"))
        if response.status_code == 200:
            self.current_ticket = response.json()["ticket"]
            return response.json()
        elif response.status_code == 404:
            return {"error": "Ticket not found."} 
    
    @authMethod
    def tasksGetRequest(self, ticket_id):
        """
        Makes a GET request to the helpdesk API to get the tasks for the ticket with the specified ID.
        Returns the tasks if the ticket exists, otherwise returns an error message.
        """
        url = self.url + "/api/v2/tickets/" + str(ticket_id) + "/tasks"
        response = requests.get(url, auth=(self.key, "X"))
        if response.status_code == 200:
            output = [task["title"] for task in response.json()["tasks"]]
            return output 
        elif response.status_code == 404:
            return {"error": "Ticket not found."}
        

    @authMethod
    def assetGetRequest(self, barcode):
        """
        Makes a GET request to the helpdesk API to search for an asset by barcode.
        If the asset exists, returns the asset data.
        If the asset does not exist, redirects to the Add New Asset page.
        """
        asset_name = f"CUI-{barcode}" 
        url = self.url + "/api/v2/assets.json"  
        params = {"query": asset_name}  
        response = requests.get(url, auth=(self.key, "X"), params=params)
        
        if response.status_code == 200:
            assets = response.json().get("assets", [])
            if assets:
                self.current_asset = assets[0]  
                return self.current_asset
            else:
                # Asset not found, redirect to Add New Asset page
                print(f"Asset {asset_name} not found. Redirecting to Add New Asset page...")
                self.addNewAsset(barcode)  # Call the function to add a new asset
                return {"error": "Asset not found. Redirected to Add New Asset page."}
        else:
            return {"error": f"Failed to retrieve assets. Status code: {response.status_code}, Response: {response.text}"}
        
    
    @authMethod
    def addNewAsset(self, barcode):
        """
        Makes a POST request to the helpdesk API to add a new asset if it does not already exist.
        """
        asset_name = f"CUI-{barcode}"
        url = self.url + "/api/v2/assets.json"
        data = {
            "asset": {
                "name": asset_name,
                "barcode": barcode,
                "type": "Hardware",  
            }
        }
        response = requests.post(url, auth=(self.key, "X"), json=data)
        if response.status_code == 201:
            print(f"New asset {asset_name} added successfully.")
            return response.json()
        else:
            print(f"Failed to add asset {asset_name}. Status code: {response.status_code}")
            return {"error": f"Failed to add asset. Status code: {response.status_code}"}
        

    @authMethod
    def filteredTicketGetRequest(self, filter):
        """
        Makes a GET request to the helpdesk API to get the tickets that match the specified filter.
        Returns the tickets if the filter exists, otherwise returns an error message.
        """
        # Check the filter to make sure it is formatted correctly
        if filter[0] != '"':
            filter = f'"{filter}'
        if filter[-1] != '"':
            filter = f'{filter}"'
        # Make the request
        url = self.url + f'/api/v2/tickets/filter?query={filter}'
        response = requests.get(url, auth=(self.key, "X"))
        # Parse the response
        if response.status_code == 200:
            self.filtered_ticket_list = response.json()["tickets"]
            return response.json()["tickets"]
        elif response.status_code == 404:
            return {"error": "Filter not found."}


    @authMethod
    def ticketPostRequest(self, ticket_id, data):
        """
        Makes a POST request to the helpdesk API to update the ticket with the specified ID.
        Returns the updated ticket if it exists, otherwise returns an error message.
        """
        if self.validKey() == False:
            return None
        url = self.url + "/api/v2/tickets/" + str(ticket_id) + ".json"
        response = requests.post(url, auth=(self.key, "X"), data=data)
        return response.json()
    

    @authMethod
    def ticketPutRequest(self, ticket_id, data):
        """
        Makes a PUT request to the helpdesk API to update the ticket with the specified ID.
        Returns the updated ticket if it exists, otherwise returns an error message.
        """
        if self.validKey() == False:
            return None
        url = self.url + "/api/v2/tickets/" + str(ticket_id) + ".json"
        response = requests.put(url, auth=(self.key, "X"), data=data)
        return response.json()
    
    
    @authMethod
    def getGroupUsers(self, group_id):
        """
        Makes a GET request to the helpdesk API to get the users in the specified group.
        Returns the users if the group exists, otherwise returns an error message.
        """
        url = self.url + "/api/v2/groups"
        response = requests.get(url, auth=(self.key, "X"))
        if response.status_code == 200:
            groups_raw = response.json()
            groups_raw = groups_raw["groups"]
            specific_group = None
            for group in groups_raw:
                if group["id"] == int(group_id):
                    specific_group = group["members"]
            return specific_group
        elif response.status_code == 404:
            return {"error": "Group not found."}


    @authMethod
    def getAllUsers(self):
        """
        Makes a GET request to the helpdesk API to get all the agents in the helpdesk.
        """
        url = self.url + "/api/v2/agents"
        response = requests.get(url, auth=(self.key, "X"))
        if response.status_code == 200:
            self.users = response.json()["agents"]
        elif response.status_code == 404:
            return {"error": "Group not found."}

    # Parsed Data Functions
    @reqTicket
    def getTicketTitle(self):
        title = self.current_ticket["subject"]
        return title

    @reqTicket
    def getTicketDescription(self):
        description = self.current_ticket["ticket"]["description"]
        return description

    @reqTicket
    def getTicketTags(self):
        tags = self.current_ticket["ticket"]["tags"]
        return tags
    
    def getUser(self, id):
        if self.users == None:
            return None
        for user in self.users:
            if user["id"] == id:
                return f"{user['first_name']} {user['last_name']}"
        return None


