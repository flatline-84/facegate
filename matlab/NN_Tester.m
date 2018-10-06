%rootFolder = '/Users/danielsosa/Documents/RMIT/2018/ZGeneral/Capstone/NeuralNetwork/out_test';
rootFolder = '/Users/danielsosa/Documents/facegate/support_programs/out_test/';


networkName = 'NN_V03_01_350,350.onnx'; % Neural network
networkAddr = ['NeuralNetworks/' networkName];   
classes = ["anger" "neutral" "scream" "smile"]; % Specify classes
% Import network
network = importONNXNetwork(networkAddr,'OutputLayerType','classification','ClassNames',classes); 

DISP_IMAGES = 0; %Set to 1 to display all images and classifications
FILE_TERM = 'm';
IMAGE_NO = 0;

ANGER_NO = 0;
NEUTRAL_NO = 0;
SMILE_NO = 0;
SCREAM_NO = 0;

ANGER_SUCCESS = 0;
NEUTRAL_SUCCESS = 0;
SMILE_SUCCESS = 0;
SCREAM_SUCCESS = 0;

TOTAL_SUCCESS = 0;


% Get a list of all files and folders in this folder.
files = dir(rootFolder);
% Get a logical vector that tells which is a directory.
dirFlags = [files.isdir];
% Extract only those that are directories.
subFolders = files(dirFlags);
% Print folder names to command window.
for k = 1 : length(subFolders)
    folder = subFolders(k).name;
    imFolder = [rootFolder folder];

    fileList = dir(imFolder);
    % Get a logical vector that tells which is a directory.
    for l = 1 : length(fileList)
        image = fileList(l).name; % name of file
        
        % Test correct file type
        C = strsplit(image,'.');
        [name,extension] = deal(C{:});
        
        C = strsplit(image,'-');
        [first,second,third] = deal(C{:});
        if ((strcmp(extension,'png'))&&(strcmp(first,FILE_TERM)))
            imLocation = [imFolder '/' image];
             
            % Classify image
            %[Yprob,category] = classify(network,image)
            inputImage = imread(imLocation);
            category = classify(network,inputImage);
            category = char(category(1));
            

            IMAGE_NO = IMAGE_NO + 1;
            
            %Increment category counter
            if (strcmp(folder,'anger'))
               ANGER_NO = ANGER_NO + 1;
            end
            
            if (strcmp(folder,'neutral'))
               NEUTRAL_NO = NEUTRAL_NO + 1;
            end
            
            if (strcmp(folder,'smile'))
               SMILE_NO = SMILE_NO + 1;
            end
            
            if (strcmp(folder,'scream'))
               SCREAM_NO = SCREAM_NO + 1;
            end                 
            
            
            if(strcmp(folder,category))
               TOTAL_SUCCESS = TOTAL_SUCCESS + 1; 
               
                %Increment category success counter
                if (strcmp(category,'anger'))
                   ANGER_SUCCESS = ANGER_SUCCESS + 1;
                end

                if (strcmp(category,'neutral'))
                   NEUTRAL_SUCCESS = NEUTRAL_SUCCESS + 1;
                end

                if (strcmp(category,'smile'))
                   SMILE_SUCCESS = SMILE_SUCCESS + 1;
                end

                if (strcmp(category,'scream'))
                   SCREAM_SUCCESS = SCREAM_SUCCESS + 1;
                end  
            end
            
            % Show image
            if(DISP_IMAGES)
                figure;
                imshow(inputImage);
                heading = 'Expected Expression: ';
                heading = [heading category];
                title(heading);
            end

            
        end
        

        
    end

end
disp(networkName);

ANGER_SUCCESS_RATE = 100*(ANGER_SUCCESS/ANGER_SUCCESS);
NEUTRAL_SUCCESS_RATE = 100*(NEUTRAL_SUCCESS/NEUTRAL_NO);
SMILE_SUCCESS_RATE = 100*(SMILE_SUCCESS/SMILE_NO);
SCREAM_SUCCESS_RATE = 100*(SCREAM_SUCCESS/SCREAM_NO);

str = 'Anger Sucess: %0.2f%%, Neutral Sucess: %0.2f%%, Smile Sucess: %0.2f%%, Scream Sucess: %0.2f%%';
out = sprintf(str, ANGER_SUCCESS_RATE, NEUTRAL_SUCCESS_RATE, SMILE_SUCCESS_RATE, SCREAM_SUCCESS_RATE);
disp(out);

SUCCESS_RATE = 100*(TOTAL_SUCCESS/IMAGE_NO);
string = 'Classified Images: %d, Successful Classifications: %d, Success Rate: %0.2f%%';
output = sprintf(string, IMAGE_NO, TOTAL_SUCCESS, SUCCESS_RATE);
disp(output);




% image = imread('/Users/danielsosa/Documents/facegate/support_programs/out_test/smile/m-daniel-4.png');
% 
% % Classify image
% %[Yprob,category] = classify(network,image)
% category = classify(network,image);
% category = char(category(1))
% 
% 
% % imTitle = strcat('Expression: ',expression);
% 
% % Show image
% figure;
% imshow(image);
% heading = 'Expected Expression: ';
% heading = [heading category];
% title(heading);
