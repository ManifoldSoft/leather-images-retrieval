

clear all;close all;clc;

path_imgDB = './256_ObjectCategories/';
addpath(path_imgDB);

path_Thumbnails = './thumbnails/';

imgFiles = dir(path_imgDB);
imgNamList = {imgFiles(~[imgFiles.isdir]).name};
clear imgFiles;
imgNamList = imgNamList';

numImg = length(imgNamList);

for i = 1:numImg
    img = imread(imgNamList{i, 1});
    thumbnail = imresize(img, [200,200]);
    fprintf('generate thumbnail of  %d image\n\n', i);
    thumbnailNameWithPath = [path_Thumbnails, imgNamList{i, 1}];
    imwrite(thumbnail, thumbnailNameWithPath);
end