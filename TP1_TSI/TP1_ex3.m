clear all; close all;

%% 3) Filtrage non linéaire : filtre médian

%------------------------- question 3 -----------------------------

figure(1)
Image = imread('flower.png');
Image2= im2double(Image);
Affichage= imshow(Image2);
title('Image d origine');

%------------------------- question 4 -----------------------------

Image_bruit=imnoise(Image2,'salt & pepper', 0.5);
figure(2)
imshow(Image_bruit);
title('Image bruitée');

%------------------------- question 5 -----------------------------

Image_corrigee=ordfilt2(Image_bruit,5,ones(3,3));

figure(3)
imshow(Image_corrigee);
title('Image corrigée ordre 5 domaine 3/3');

%------------------------- question 6 -----------------------------
figure(4)

subplot(2,2,1);
Image_corrigee_1=ordfilt2(Image_bruit,1,ones(3,3));
imshow(Image_corrigee_1);
title('Image corrigée ordre 1 domaine (3,3)');

subplot(2,2,2);
Image_corrigee_2=ordfilt2(Image_bruit,3,ones(3,3));
imshow(Image_corrigee_2);
title('Image corrigée ordre 3 domaine (3,3)');

subplot(2,2,3);
Image_corrigee_3=ordfilt2(Image_bruit,5,ones(3,3));
imshow(Image_corrigee_3);
title('Image corrigée ordre 5 domaine (3,3)');

subplot(2,2,4);
Image_corrigee_4=ordfilt2(Image_bruit,7,ones(3,3));
imshow(Image_corrigee_4);
title('Image corrigée ordre 7 domaine (3,3)');



figure(5)

subplot(2,2,1);
Image_corrigee_5=ordfilt2(Image_bruit,((3*3+1)/2 ),ones(3,3));
imshow(Image_corrigee_5);
title('Image corrigée avec filtre median domaine (3,3)');

subplot(2,2,2);
Image_corrigee_6=ordfilt2(Image_bruit,((5*5+1)/2 )+1,ones(5,5));
imshow(Image_corrigee_6);
title('Image corrigée avec filtre median domaine (5,5)');

subplot(2,2,3);
Image_corrigee_7=ordfilt2(Image_bruit,((7*7+1)/2 )+1,ones(7,7));
imshow(Image_corrigee_7);
title('Image corrigée avec filtre median domaine (7,7)');

subplot(2,2,4);
Image_corrigee_8=ordfilt2(Image_bruit,((9*9+1)/2 )+1,ones(9,9));
imshow(Image_corrigee_8);
title('Image corrigée avec filtre median domaine (9,9)');

