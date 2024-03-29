"""
MIT License

Copyright (c) 2021-2022 Jun Jay Ng

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

#game set-up
import random
import threading
import time
import datetime
import requests

#variables
gameRunning = True
sentences = []
timeLeft = t = 60*1

#player score
#structure: [p1 score, p2 score, p3 score and so on...]
scores = []

#themes lmao
themes = { 
  #Structure: {theme:[sentences]}
  'Flight':['There once was a flying pig', 
            'The rocket was beside the plane',
            'The man invented a portable wing',
            ],
  'Fairy Tale':[
            'Once upon a time....',
            'There once was a princess',
            'Her hair was long, ',
            ],
  'Social Media':[
            'The media is a reliable source of information',
            'Social media is the way of communication'
            ],
  'Studies':[
            'Studying is',
            ],
}

#select a theme from the dict
theme = random.choice(list(themes.keys()))
#select a sentence from the dict
sentence_selected = random.choice(list(themes[theme]))

#get the number of players
player_no = input("Number of players: ")
player_names= []
while True:
  try:
    player_no = int(player_no)
    if player_no > 0:break
    raise ValueError
  except ValueError:
    print("Invalid Input!")
    print("Value must be a number, and more than 1.")
    player_no = input("Number of players: ")


#get the name of players
for i in range(player_no):
  name = input(f"Player {i+1}'s name: ")
  player_names.append(name)
  scores.append(0)

#set timer thread
def countdown(t):
    global gameRunning, timeLeft
    while t > 0:
      mins = t // 60
      secs = t % 60
      #timer = '{:02d}:{:02d}'.format(mins, secs)
      time.sleep(1)
      timeLeft -= 1
      t -= 1
    gameRunning = False
#set time
timerThread = threading.Thread(target=countdown,args=(t,))
#give instruction
print('''/\I  ''')
print("\n\n-----------\nYou guys have 10 minutes to come up with story :)\n")

#start timer
timerThread.start()
#print(timerThread, end="\r")

#get AI response
def getAIresponse():
  if len(sentences) > 1:
    string = sentences[-2] + sentences[-1] 
  else:
    string = sentences[-1]
  r = requests.post("https://api.deepai.org/api/text-generator",data={'text': string},headers={'api-key':'8d73203a-4c9b-464d-8e8c-df5b0f6934a0'})
  r = r.json()
  return (r['output'].split('\n')[0])[len(string):]

#story time
if gameRunning:
  print(f"the theme generated is: \n{theme}\n")
  #just a space to seperate theme from starter senetence
  print('the starter sentence is: ')
  print(sentence_selected + "\n\n\n-----------")
  print("Type a word and click Enter on your keyboard to start the game!")

while gameRunning:
  if not gameRunning: break
  for i in range(player_no):
    if not gameRunning: break
    print(f'{player_names[i]}\'s turn: ({str(datetime.timedelta(seconds=timeLeft))} left)')
    ans = input('> ')
    sentences.append(ans)
    scores[i] += len(ans.split(' '))
  
  #AI response
  print('AI\'s response: ')
  print('> ', end='')
  if not gameRunning: break #check if time's up
  response = getAIresponse()
  print(response)
  sentences.append(response)



print("\n\n-----------\ntime is up!")
print('the story you guys made is....')
print(sentence_selected + ' ' + ' '.join(sentences) + '\n')
print('\n-----------\nScores:')
for i in range(len(scores)):
  print(f'{player_names[i]}: {scores[i]}')

indices = [i for i, x in enumerate(scores) if x == scores[scores.index(max(scores))]]
if len(indices) > 1:
  print('\nDraw!')
else:
  print(f'\nWinner: {player_names[scores.index(max(scores))]}')

total = 0
for x in scores:
  total += x
print(f'\nTotal Score: {total}')
