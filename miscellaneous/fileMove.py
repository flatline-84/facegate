import os


# 1 : Neutral expression
# 2 : Smile
# 3 : Anger
# 4 : Scream

# os.chdir('/Users/danielsosa/Documents/RMIT/2018/ZGeneral/Capstone/NeuralNetwork/data/imageData')

for f in os.listdir('/Users/danielsosa/Documents/RMIT/2018/ZGeneral/Capstone/NeuralNetwork/data/imageData'):
    file_name, file_ext = os.path.splitext(f)
    #file_name, disc = os.path.splitext(file_name) #split again to remove .raw
    gender, uid, expression = file_name.split('-')
    #new_name = '{}-{}-{}{}'.format(gender, uid, expression, file_ext)
    # print gender, uid, expression
    original = '/Users/danielsosa/Documents/RMIT/2018/ZGeneral/Capstone/NeuralNetwork/data/imageData/' + f

    if expression == '1':
        #move to neutral
        print('neutral')
        f_new = '/Users/danielsosa/Documents/RMIT/2018/ZGeneral/Capstone/NeuralNetwork/data/neutral/' + f
        os.rename(original, f_new)
    elif expression == '2':
        #move to smile
        print('smile')
        f_new = '/Users/danielsosa/Documents/RMIT/2018/ZGeneral/Capstone/NeuralNetwork/data/smile/' + f
        os.rename(original, f_new)
    elif expression == '3':
        #move to anger
        print('anger')
        f_new = '/Users/danielsosa/Documents/RMIT/2018/ZGeneral/Capstone/NeuralNetwork/data/anger/' + f
        os.rename(original, f_new)
    elif expression == '4':
        #move to scream
        print('scream')
        f_new = '/Users/danielsosa/Documents/RMIT/2018/ZGeneral/Capstone/NeuralNetwork/data/scream/' + f
        os.rename(original, f_new)

    elif expression == '14':
        #move to neutral
        print('neutral')
        f_new = '/Users/danielsosa/Documents/RMIT/2018/ZGeneral/Capstone/NeuralNetwork/data/neutral/' + f
        os.rename(original, f_new)
    elif expression == '15':
        #move to smile
        print('smile')
        f_new = '/Users/danielsosa/Documents/RMIT/2018/ZGeneral/Capstone/NeuralNetwork/data/smile/' + f
        os.rename(original, f_new)
    elif expression == '16':
        #move to anger
        print('anger')
        f_new = '/Users/danielsosa/Documents/RMIT/2018/ZGeneral/Capstone/NeuralNetwork/data/anger/' + f
        os.rename(original, f_new)
    elif expression == '17':
        #move to scream
        print('scream')
        f_new = '/Users/danielsosa/Documents/RMIT/2018/ZGeneral/Capstone/NeuralNetwork/data/scream/' + f
        os.rename(original, f_new)


