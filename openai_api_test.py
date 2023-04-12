import os

import openai

openai.api_key = os.environ['OPENAPI_API_KEY']
# prompt = "Hello, this is a test, if you can receive this message, just reply: ChatGPT system online."

prompt='this is a syllubus for a fluid dynamics course. please read and answer the following questions.'
prompt+='''
Course Title: Fluid Dynamics (Summer 2023)

Instructor: [Insert Name]
Email: [Insert Email]

Course Description:
This course provides an introduction to fluid dynamics and its applications. Topics covered include fluid statics, fluid kinematics, conservation laws, flow in pipes and ducts, and boundary layer theory. Students will gain an understanding of the fundamental principles governing fluid flow and develop analytical and problem-solving skills through homework assignments and a final project.

Course Schedule:

Week 1 (May 1 - May 7):

Lecture 1: Introduction to Fluid Dynamics
Lecture 2: Fluid Statics
Week 2 (May 8 - May 14):

Lecture 3: Fluid Kinematics
Quiz 1 (May 10)
Week 3 (May 15 - May 21):

Lecture 4: Conservation Laws
Assignment 1 Due (May 17)
Week 4 (May 22 - May 28):

Lecture 5: Flow in Pipes and Ducts
Reading Week (May 24 - May 28)
Week 5 (May 29 - June 4):

Lecture 6: Dimensional Analysis and Similitude
Lecture 7: Boundary Layer Theory
Week 6 (June 5 - June 11):

Lecture 8: Viscous Flow and Flow Past Immersed Bodies
Assignment 2 Due (June 7)
Week 7 (June 12 - June 18):

Lecture 9: Turbulent Flow
Quiz 2 (June 14)
Week 8 (June 19 - June 25):

Lecture 10: Introduction to Computational Fluid Dynamics
Final Project Proposal Due (June 23)
Week 9 (June 26 - July 2):

Lecture 11: Applications of Fluid Dynamics
Assignment 3 Due (June 30)
Week 10 (July 3 - July 9):

Lecture 12: Review of Course Material
Final Project Progress Report Due (July 7)
Week 11 (July 10 - July 16):

Final Project Presentations (July 12 - July 16)
Finals Week (July 17 - July 23):

Final Project Report Due (July 21)
Grading:

Assignment 1: 15%
Assignment 2: 15%
Assignment 3: 20%
Quiz 1: 10%
Quiz 2: 10%
Final Project Proposal: 5%
Final Project Progress Report: 5%
Final Project Presentation: 10%
Final Project Report: 10%
'''

prompt+="hello professor, when is the reading week?"

# Completion does not have conversation context, have to load all given knowledge
# response = openai.Completion.create(
#         model="text-curie-001", prompt=prompt, temperature=0.0)

messages=[
{"role": "system", "content": "You are a helpful assistant."},
{"role": "user", "content": "Who won the world series in 2020?"},
{"role": "assistant", "content": "The Los Angeles Dodgers won the World Series in 2020."},
{"role": "user", "content": "Where was it played?"}
]

response = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",

)
# get message from user
print(response["choices"][0]["message"])
#  append message to messages
messages.append({"role": "assistant", "content": response["choices"][0]["text"]})