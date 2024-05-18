with open('MY_LOG.txt', 'w') as f:
    f.write('')

def log(text):
    with open('MY_LOG.txt', 'a') as f:
        f.write(text + '\n')