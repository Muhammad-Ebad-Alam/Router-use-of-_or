#type: ignore
from crewai.flow.flow import Flow, listen, start, router, or_
from litellm import completion
import random
import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file
load_dotenv(find_dotenv())

# Get API key with error handling
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

class RouterFlow(Flow):

    @start()
    def input(self):

        cities = ["Karachi","Lahore","Quetta"]
        select_city = random.choice(cities)
        self.state['city'] = select_city

    @router('input')
    def select_city(self):
        
        if self.state['city'] == "Karachi":
            return 'Karachi'
        elif self.state['city'] == "Lahore":
            return 'Lahore'
        elif self.state['city'] == "Quetta":
            return 'Quetta'
        else:
            return ("none")
    
    

    @listen('Karachi')
    def karachi(self):
        response = completion(
            api_key=os.getenv("GOOGLE_API_KEY"),
            model="gemini/gemini-1.5-flash",
            messages=[
                {"role": "user", "content": f"Write some fun fact about {self.state['city']} city"}
            ],
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content

    @listen('Lahore')
    def lahore(self):
        response = completion(
            model="gemini/gemini-1.5-flash",
            api_key = os.getenv("GOOGLE_API_KEY"),
            messages=[
                {"role": "user", "content": f"Write some fun fact about {self.state['city']} city"}
            ],
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content

    @listen('Quetta')
    def quetta(self):
        response = completion(
            model="gemini/gemini-1.5-flash",
            api_key=os.getenv("GOOGLE_API_KEY"),
            messages=[
                {"role": "user", "content": f"Write some fun fact about {self.state['city']} city"}
                    ],
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content
    @listen(or_('karachi','quetta','lahore'))   
    def save_as_readme(self,result):
        with open("README.md","w") as f:
            f.write(result)
        print("File saved as README.md")   

def kickoff():
    obj = RouterFlow()
    obj.kickoff()
    


    # ebad