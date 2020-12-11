
start_pos = '000000912.01.01'

state_to_write = False
new_word = ''
for char in start_pos:
    if char != '0':
        state_to_write = True
    if state_to_write:
        new_word += char
    print(new_word)
start_pos = new_word

