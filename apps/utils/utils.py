import random
from random import choice
from random import SystemRandom

from datetime import datetime

def random_code(len_code):
  cryptogen = SystemRandom()
  valores = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  code = []
  for i in range(len_code):
    code.append(cryptogen.choice(valores))  
  return "".join(code)


def now_date():
  now_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
  return now_date


def random_code1(len_code):
  letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
  code = []
  for i in range(len_code):
    if i%2==0:
      code.append(str(random.randint(0, 9)))     
    else:
      code.append(choice(letters))

  result = "".join(code)
  return result

def random_code2(len_code):
  valors = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
  code = ""
  code = code.join([choice(valors) for i in range(len_code)])
  
  return code