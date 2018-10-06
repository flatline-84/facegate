import os


# 1 : Neutral expression
# 2 : Smile
# 3 : Anger
# 4 : Scream

# os.chdir('/Users/danielsosa/Documents/RMIT/2018/ZGeneral/Capstone/NeuralNetwork/data/imageData')

for f in os.listdir('/Users/danielsosa/Documents/facegate/support_programs/out_test/anger'):
    if (f[0] == '.'):
        continue
    file_name, file_ext = os.path.splitext(f)
    # print(file_name)
    #file_name, disc = os.path.splitext(file_name) #split again to remove .raw
    gender, name, number = file_name.split('-')
    #new_name = '{}-{}-{}{}'.format(gender, uid, expression, file_ext)
    # print gender, uid, expression
    original_dir = '/Users/danielsosa/Documents/facegate/support_programs/out_test/anger/'
    original = '/Users/danielsosa/Documents/facegate/support_programs/out_test/anger/' + f

    if ((int(number) > 15) and (int(number) < 125)):
        number = int(number) + 109
        new_name = '{}-{}-{}{}'.format(gender, name, number, file_ext)
        f_new = original_dir + new_name
        os.rename(original, f_new)
        print(original)
        print(f_new)
