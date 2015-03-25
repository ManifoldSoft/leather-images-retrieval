
clear;
addpath('./contest_data/clothes/clothes_source/');
addpath('./contest_data/clothes/clothes_image/');
addpath('./rootHSV/')

imgFiles = dir('./contest_data/clothes/clothes_source/');
imgQueryNamList = {imgFiles(~[imgFiles.isdir]).name};
clear imgFiles;

bins = [20, 10, 5]; % 1000-dim HSV histogram
%bins = [40, 20, 10]; % 8000-dim HSV histogram

imgQueryNamList = imgQueryNamList';

numImgQuery = length(imgQueryNamList);
feat = [];
k = 0;
rgbImgList = {};

for i = 1:numImgQuery
   oriImg = imread(imgQueryNamList{i, 1});
   if size(oriImg, 3) ~= 3
       rgbImg(:,:,1) = oriImg;
       rgbImg(:,:,2) = oriImg;
       rgbImg(:,:,3) = oriImg;
   else
       rgbImg = oriImg;
   end
   img = double(rgbImg)./255;  
   featVec = hsvhist(img, bins);
   feat = [feat; featVec];
   fprintf('extract rootHSV feature of %d image\n\n', i);
end

queryHist = feat';

% calculate rootHSV (HSV*)
sum_val = sum(queryHist); % 1*10200
d = bins(1)*bins(2)*bins(3);
for n = 1:d
    queryHist(n, :) = queryHist(n, :)./sum_val;
end
queryHist = sqrt(queryHist);

%save('clothesQuery8000RootHSV.mat','queryHist', 'imgQueryNamList');
save('clothesQuery1000RootHSV.mat','queryHist', 'imgQueryNamList');

%load clothes8000RootHSV.mat;
load clothes1000RootHSV.mat;

queryID = 1;

numImg = length(imgNamList);

queryhist = queryHist(:, queryID);
dist = zeros(numImg, 1);
for i = 1:numImg
    dist(i) = sum(abs(queryhist-Hist(:, i)));
end
[~, rank] = sort(dist, 'ascend');

numShow = 50;

I2 = uint8(zeros(100, 100, 3, numShow)); % 32 and 32 are the size of the output image
for i=1:numShow
    im = imread(imgNamList{rank(i, 1), 1});
    
    outPutImgFile = sprintf('./share/%d.jpg',i);
    imwrite(im, outPutImgFile);
    
    queryRootHSV51List{i,1} = imgNamList{rank(i, 1), 1};
    im = imresize(im, [100 100]);
    if (ndims(im)~=3)
        I2(:, :, 1, i) = im;
        I2(:, :, 2, i) = im;
        I2(:, :, 3, i) = im;
    else
        I2(:, :, :, i) = im;
    end
end

queryRootHSV51List{numShow+1,1} = imgQueryNamList{queryID, 1};

im = imread(imgQueryNamList{queryID, 1});
im = imresize(im, [100 100]);
imshow(im);

im = imread(imgQueryNamList{queryID, 1});
outPutImgFile = sprintf('./share/%d.jpg', numShow+1);
imwrite(im, outPutImgFile);

figure('color',[1,1,1]);
montage(I2(:, :, :, (1:numShow)));