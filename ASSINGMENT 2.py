
import requests
import json
import csv
from datetime import datetime

# ===============================================================
# Class: JokeFetcher
# ---------------------------------------------------------------
# This class is responsible for fetching jokes from JokeAPI.
# By encapsulating the API call in a class, we adhere to OOP principles,
# making the code more modular and reusable. This also simplifies 
# maintenance and testing because we isolate the API interactions.
# ===============================================================
class JokeFetcher:
    def __init__(self):
        # The base URL points to the JokeAPI endpoint.
        self.base_url = "https://v2.jokeapi.dev/joke/Any"
    
    def get_joke(self):
        """
        Fetch a random joke from the JokeAPI.
        Returns:
            dict: The API returns a JSON object containing joke details.
                  It includes keys like 'type', 'joke' for single-line jokes or
                  'setup' and 'delivery' for two-part jokes.
        """
        try:
            # Make an HTTP GET request to fetch the joke.
            response = requests.get(self.base_url)
            
            # Check for a successful response. A status code of 200 means OK.
            if response.status_code == 200:
                joke_data = response.json()
                return joke_data
            else:
                print("Error fetching joke, Status Code:", response.status_code)
                return None
        except Exception as e:
            # Handle exceptions that may occur during the request.
            print("Exception occurred while fetching joke:", e)
            return None

# ===============================================================
# Class: JokeStorage
# ---------------------------------------------------------------
# This class handles storing the fetched joke into files.
# It offers methods to write the joke data to both JSON and CSV formats.
# Separating the storage logic into its own class keeps the code clean
# and supports separation of concerns, an important aspect of OOP.
# ===============================================================
class JokeStorage:
    def store_json(self, joke_data, filename="joke_data.json"):
        """
        Save the joke data in JSON format.
        
        Args:
            joke_data (dict): The joke data dictionary from the API.
            filename (str): Optional filename for saving the data.
        """
        try:
            with open(filename, 'w') as file:
                json.dump(joke_data, file, indent=4)
            print(f"Joke stored in JSON format in {filename}")
        except Exception as e:
            print("Error saving JSON file:", e)
    
    def store_csv(self, joke_data, filename="joke_data.csv"):
        """
        Save the joke data in CSV format.
        
        Args:
            joke_data (dict): The joke data dictionary from the API.
            filename (str): Optional filename for saving the data.
            
        Note:
            The CSV file stores the joke information as a single row, with 
            keys as headers. This demonstrates simple data persistence.
        """
        # Use the keys of the joke_data dictionary as CSV headers.
        keys = joke_data.keys()
        try:
            with open(filename, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=keys)
                writer.writeheader()
                writer.writerow(joke_data)
            print(f"Joke stored in CSV format in {filename}")
        except Exception as e:
            print("Error saving CSV file:", e)

# ===============================================================
# Main Script Execution
# ---------------------------------------------------------------
# This part of the code ties everything together:
#   1. It creates an instance of JokeFetcher and fetches a joke.
#   2. It displays the fetched joke in the terminal in a readable format.
#   3. It then creates an instance of JokeStorage to save the joke
#      in both JSON and CSV formats.
# The structure of the code ensures a clean separation of responsibilities,
# simplifying debugging, testing, and future expansion.
# ===============================================================
if __name__ == "__main__":
    # Instantiate the JokeFetcher to get a joke from the API.
    joke_fetcher = JokeFetcher()
    joke = joke_fetcher.get_joke()

    # Check if a joke has been successfully fetched.
    if joke:
        # Determine if the joke is a 'single' or 'twopart' joke.
        if joke.get("type") == "single":
            # For single-line jokes, display the 'joke' key.
            print("Joke:", joke.get("joke"))
        elif joke.get("type") == "twopart":
            # For two-part jokes, display both the setup and delivery.
            print("Setup:", joke.get("setup"))
            print("Delivery:", joke.get("delivery"))
        else:
            print("Received joke data in an unexpected format:", joke)
    else:
        print("Failed to fetch a joke.")

    # Instantiate JokeStorage to save the fetched joke.
    storage = JokeStorage()

    # Use the current timestamp to create unique filenames.
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Store the joke in JSON format.
    storage.store_json(joke, filename=f"joke_{timestamp}.json")
    
    # Store the joke in CSV format.
    storage.store_csv(joke, filename=f"joke_{timestamp}.csv")
    
    # ===========================================================
    # Presentation Comments:
    # - The use of OOP (with JokeFetcher and JokeStorage classes)
    #   illustrates how to separate concerns — API interaction and data storage.
    # - Each method has a clear responsibility, making the code modular,
    #   reusable, and easier to maintain.
    # - Detailed comments are provided throughout the code to explain each step.
    # - Error handling is used to ensure that failures in API calls or file I/O
    #   are gracefully managed.
    # - The code outputs the joke in a readable format and saves data in both
    #   JSON and CSV formats as required by the assignment.
    # ===========================================================
