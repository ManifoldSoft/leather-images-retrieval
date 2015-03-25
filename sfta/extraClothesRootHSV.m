
clear;
addpath('./contest_data/clothes/clothes_image/');
addpath('./rootHSV/')

imgFiles = dir('./contest_data/clothes/clothes_image');
imgNamList = {imgFiles(~[imgFiles.isdir]).name};
save('clothes_image.mat','imgNamList', '-v7.3');
clear imgFiles;



bins = [40, 20, 10]; % 8000-dim HSV histogram
%bins = [20, 10, 5]; % 1000-dim HSV histogram

imgNamList = imgNamList';

numImg = length(imgNamList);
feat = [];
k = 0;
rgbImgList = {};

matlabpool;

parfor i = 1:numImg
   oriImg = imread(imgNamList{i, 1});
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

matlabpool close;

Hist = feat';

% calculate rootHSV (HSV*)
sum_val = sum(Hist); % 1*10200
d = bins(1)*bins(2)*bins(3);
for n = 1:d
    Hist(n, :) = Hist(n, :)./sum_val;
end
Hist = sqrt(Hist);

save('clothes8000RootHSV.mat','Hist', 'imgNamList', '-v7.3');
%save('clothes1000RootHSV.mat','Hist', 'imgNamList', '-v7.3');


% queryID = 11;
% 
% queryhist = Hist(:, queryID);
% dist = zeros(numImg, 1);
% for i = 1:numImg
%     dist(i) = sum(abs(queryhist-Hist(:, i)));
% end
% [~, rank] = sort(dist, 'ascend');
% 
% numShow = 50;
% 
% I2 = uint8(zeros(100, 100, 3, numShow)); % 32 and 32 are the size of the output image
% for i=1:numShow
%     im = imread(imgNamList{rank(i, 1), 1});
%     im = imresize(im, [100 100]);
%     if (ndims(im)~=3)
%         I2(:, :, 1, i) = im;
%         I2(:, :, 2, i) = im;
%         I2(:, :, 3, i) = im;
%     else
%         I2(:, :, :, i) = im;
%     end
% end
% 
% figure('color',[1,1,1]);
% montage(I2(:, :, :, (1:numShow)));