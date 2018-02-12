"""

2-8-2018

The purpose of this code is to transfer consumer survey data from an excel
spreadsheet into a Neo4j graph database.

@author: eadlaf

"""


import pandas as pd
import numpy as np
from py2neo import authenticate, Graph, Node, Relationship

# load the excel data into a pandas dataframe
data = pd.read_excel('F:/Tivo/Data Science Projects/Q4SurveyA-BO.xlsx')
# name the business quarter that the survey data was collected
quarter_year = 'Q42017'

# set up authentication parameters for the local neo4j server
authenticate('localhost:7687', 'user', 'pass')
# connect to the local instance of neo4j with created password
graph = Graph(password='mango')


# slice the dataframe for the indexes and rows of choice
questions = [val for val in data.columns[1:5]]
answers = data.iloc[1:4, 1:5]
respondents = data.iloc[1:4, 0]

# define ranges for the number of questions and answers
ques_num = range(len(questions))
ans_num = range(len(answers))

# define a function to enter respondent and answer data for one question
def populateDB(x):
    q = Node('Question', question=questions[x]) # enters the question title at index 'x' as a node

    for y in ans_num:
        a = Node('Answer', response=answers.iloc[y, x], quarter=quarter_year)
        r = Node('Respondent', ID=respondents.iloc[y])
        qa = Relationship(q, 'Contains', a)
        ar = Relationship(a, 'From', r)
        graph.create(qa)
        graph.create(ar)

for i in ques_num:
    populateDB(i)

# add nodes and relationships individually
# r = Node('Respondent', ID=respondents.iloc[0])
# a = Node('Answer', response=answers.iloc[0, 1], quarter=quarters[4])
# q = Node('Question', question=questions[0])
# qa = Relationship(q, 'Contains', a)
# ar = Relationship(a, 'From', r)
# # ra = Relationship(r, 'Answered', a)
# # aq = Relationship(a, 'InResponseTo', q)
# graph.create(qa)
# graph.create(ar)


# import question nodes
# for index in questions:
#     graph.create(Node('Question', question=index))
#
# for row in respondents:
#     graph.create(Node('Respondent', ID=row))
