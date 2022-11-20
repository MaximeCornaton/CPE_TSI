clear all;
close all;

Image=imread('guigs.jpg');
imwrite(Image,'guigs.ppm');
Image_ppm=imread('guigs.ppm');

figure(1);
imshow('guigs.jpg');

figure(2)
subplot(3,1,1);
imshow(Image(:,:,1));
title('image niveau de gris rouge')
subplot(3,1,2);
imshow(Image(:,:,2));

title('image niveau de gris vert')
subplot(3,1,3);
imshow(Image(:,:,3));
title('image niveau de gris bleu')

figure(3)
nL=416;
nC=752;
nCx=3;

Z=uint8(zeros(nL,nC,nCx));
subplot(3,1,1);
Z(:,:,1)=Image(:,:,1);
imshow(Z);
title('image rouge')
Z(:,:,1)=0;

subplot(3,1,2);
Z(:,:,2)=Image(:,:,2);
imshow(Z);
title('image vert')
Z(:,:,2)=0;
subplot(3,1,3);
Z(:,:,3)=Image(:,:,3);
imshow(Z);
title('image bleu')
Z(:,:,3)=0;

matrice=[1,0,1.13983;1,-0.39465,-0.58060;1,2.03211,0];
matrice1=inv(matrice);


HSV_image=rgb2hsv(Image);

figure(4)
subplot(3,1,1);
imshow(HSV_image(:,:,1));
title('image représentantla couleur (teinte)')
subplot(3,1,2);
imshow(HSV_image(:,:,2));

title('image niveau de gris vert')
subplot(3,1,3);
imshow(HSV_image(:,:,3));
title('image niveau de gris bleu')