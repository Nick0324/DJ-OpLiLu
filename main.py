from command_implementations import client

file = open('token.txt', 'r')
client.run(file.readline())
file.close()
