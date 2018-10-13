% outputFolder = fullfile(MacintoshHD/User/danielsosa/Documents/RMIT/2018/Capstone/NeuralNetwork, 'caltech101'); % define output folder
rootFolder = '/Users/danielsosa/Documents/RMIT/2018/ZGeneral/Capstone/NeuralNetwork/data';
categories = {'anger', 'neutral', 'smile', 'scream'};
imds = imageDatastore(fullfile(rootFolder, categories), 'LabelSource', 'foldernames');

%Split data into training and validation data
[imdsTrain,imdsValidation] = splitEachLabel(imds,0.7,'randomized');



%% 
% Layer specification
layers = [
    imageInputLayer([576 768 1])
    
    convolution2dLayer(7,8,'Padding',1) % First argument = filter size, second = num of filters
    batchNormalizationLayer
    reluLayer
    
    maxPooling2dLayer(2,'Stride',2)
    
    convolution2dLayer(5,16,'Padding',1)
    batchNormalizationLayer
    reluLayer
    
    maxPooling2dLayer(2,'Stride',2)
    
    convolution2dLayer(3,32,'Padding',1)
    batchNormalizationLayer
    reluLayer
    
    maxPooling2dLayer(2,'Stride',2)

    
    convolution2dLayer(3,64,'Padding',1)
    batchNormalizationLayer
    reluLayer
    
    maxPooling2dLayer(2,'Stride',2)
    
    fullyConnectedLayer(4) % 4 because there are 4 output classes (expressions)
    softmaxLayer
    classificationLayer];

%%
inputSize =  [576,768];%net.Layers(1).InputSize;    % Input size of first layer

%%
% Training options

% options = trainingOptions('sgdm', ...
%     'MaxEpochs',5, ...
%     'ValidationData',imdsValidation, ...
%     'ValidationFrequency',30, ...
%     'Verbose',false, ...
%     'Plots','training-progress');

% Optional data augmentation for reduce network image recognition
pixelRange = [-30 30];
imageAugmenter = imageDataAugmenter( ...
    'RandXReflection',true, ...
    'RandXTranslation',pixelRange, ...
    'RandYTranslation',pixelRange);
augimdsTrain = augmentedImageDatastore(inputSize(1:2),imdsTrain, ...
    'DataAugmentation',imageAugmenter);

augimdsValidation = augmentedImageDatastore(inputSize(1:2),imdsValidation);


options = trainingOptions('sgdm', ...
    'Momentum', 0.9000, ...
    'InitialLearnRate', 0.0100, ...
    'MiniBatchSize',10, ...
    'MaxEpochs',5, ...
    'InitialLearnRate',1e-4, ...
    'ValidationData',augimdsValidation, ...
    'ValidationFrequency',3, ...
    'ValidationPatience',100, ... % Cap for speed. def is inf
    'Verbose',false ,...
    'Plots','training-progress');

%%

%%
% Train Network


net = trainNetwork(imdsTrain,layers,options);

%%

