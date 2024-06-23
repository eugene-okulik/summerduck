my_num = 34


# while True:
#     user_num = int(input('your num: '))
#     if user_num == my_num:
#         break
#     elif user_num > my_num:
#         print('число должно быть меньше')
#     else:
#         print('число должно быть больше')


while (user_num := int(input('your num: '))) != my_num:
    if user_num > my_num:
        print('число должно быть меньше')
    else:
        print('число должно быть больше')

print('Congrats!')

while True:
    user_input = input('say something: ')
    match user_input:
        case 'hello':
            print('hi')
        case 'bye':
            print('good bye')
        case '.':
            print('finishing, bye!')
            break
        case _:
            print('hi, bye?')
