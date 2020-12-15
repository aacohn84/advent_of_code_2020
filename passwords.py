def isValidPassword1(line):
  parts = line.split(' ')
  # parts[0] '1-3'
  # parts[1] 'a:'
  # parts[2] 'ankjdhbaaaaa'
  part1 = parts[0].split('-')
  low = int(part1[0])
  high = int(part1[1])
  char = parts[1][0]
  count = 0
  for s in parts[2]:
    if s == char:
      count += 1
      if (count > high):
        return False
  return (count >= low and count <= high)

def isValidPassword2(line):
  parts = line.split(' ')
  # parts[0] '1-3'
  # parts[1] 'a:'
  # parts[2] 'ankjdhbaaaaa'
  part1 = parts[0].split('-')
  p1 = int(part1[0]) - 1
  p2 = int(part1[1]) - 1
  char = parts[1][0]
  pos1 = parts[2][p1] == char
  pos2 = parts[2][p2] == char
  return pos1 ^ pos2

def getInputs(filename):
  store = []
  file = open(filename, 'r')
  lines = file.readlines()
  for line in lines:
    store.append(line.strip())
  return store

def getNumValidPasswords(inputs):
  count = 0
  for line in inputs:
    if isValidPassword2(line):
      count += 1
  return count

print(getNumValidPasswords(getInputs('passwords.txt')))