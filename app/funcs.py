import random
def CheckID(ID) :
 if(len(ID)!=9) :
  return False

 IdList = list()

 try :
  id = list(map(int, ID))
 except :
  return False

 counter = 0

 for i in range(9) :
  id[i] *= (i%2) +1
  if(id[i]>9) :
   id[i] -=9
  counter += id[i]

 if(counter%10 == 0) :
  return True
 else :
  return False

def GenerateID():
    while True:
        id = [str(random.randint(0, 9)) for _ in range(9)]
        if CheckID(id):
            return "".join(id)


