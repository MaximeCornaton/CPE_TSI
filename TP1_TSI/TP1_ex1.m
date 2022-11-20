clear all; close all;

%% 1) Filtrage passe-haut dans l’espace direct : détection de contours


%------------------------- question 1 ---------------------------------

filt = [1;2;1];     % matrice de filtrage
deriv= [-1,0,1];    % matrice de derivation

A=(filt)*deriv;     % matrice 3x3
B=(deriv')*(filt'); % matrice 3x3


%-------------------------- question 2 -------------------------------

figure(1)
Image = imread('flower.png');
Image2= im2double(Image);
Affichage= imshow(Image2);
title('Image d origine');


%------------------------- question 3 ---------------------------------

Gx=imfilter(Image2,A);  % traitement de l'image horizontal
Gy=imfilter(Image2,B);  % traitement de l'image vertical

figure(2)
subplot(1,2,1)
imshow(Gx,[]) % affiche la composante horizontale (Gh)
title('traitement horizontal');

subplot(1,2,2)
imshow(Gy,[]) % affiche la composante verticale (Gv)
title('traitement vertical');

figure(3)
quiver(Gx,Gy), axis ij;  % affiche le gradient en chaque pixel de l'image
title('gradient en chaque pixel');


%------------------------- question 4 -----------------------------

G= sqrt(Gx.^2 +Gy.^2);% Calcul de la norme des gradients

figure(4)

subplot(2,2,1)
imshow( Image2);
title('Image originale');

subplot(2,2,2)
imshow(imcomplement(G),[]);
title('Norme du gradient en chaque pixel');

subplot(2,2,3)
imshow( imcomplement(Gx),[]);
title('traitement horizontal');


subplot(2,2,4)
imshow( imcomplement(Gy),[])
title('traitement vertical');


%------------------------- question 5 -----------------------------

Image_bruit=imnoise(Image2,'gaussian',0,0.01);
GxB=imfilter(Image_bruit,A);  % traitement de l'image horizontal
GyB=imfilter(Image_bruit,B);  % traitement de l'image vertical

figure(5)
Affichage_Image_Bruit= imshow(Image_bruit);
title('Image bruitée');

figure(6)
subplot(1,2,1)
imshow(GxB,[]) % affiche la composante horizontale (Gh)
title('traitement horizontal');

subplot(1,2,2)
imshow(GyB,[]) % affiche la composante verticale (Gv)
title('traitement vertical');

figure(7)
quiver(GxB,GyB), axis ij;  % affiche le gradient en chaque pixel de l'image
title('gradient en chaque pixel');

GB= sqrt(GxB.^2 +GyB.^2)+0.00000001; % on ajoute un trés faible nombre pour que le résultat ne soit pas 0 car on divise par GB plus tard  

figure(8)

subplot(2,2,1)
imshow( Image_bruit);
title('Image bruitée');

subplot(2,2,2)
imshow(imcomplement(GB),[]);
title('Norme du gradient en chaque pixel');

subplot(2,2,3)
imshow( imcomplement(GxB),[]);
title('traitement horizontal');

subplot(2,2,4)
imshow( imcomplement(GyB),[])
title('traitement vertical');

%------------------------- question 6 -----------------------------

GyB_n = GyB./G; % Composantes normalisées
GxB_n = GxB./G;

%------------------------- question 7 -----------------------------


d = 2; % Distance


[A,B] = meshgrid(1:256,1:256);

p1_x = A + round(GxB_n*d);
p1_x(p1_x<1) = 1;
p1_x(p1_x>256) = 256;

p1_y = B + round(GyB_n*d);
p1_y(p1_y<1) = 1;
p1_y(p1_y>256) = 256;

p2_x = A - round(GxB_n*d);
p2_x(p2_x<1) = 1;
p2_x(p2_x>256) = 256;

p2_y = B - round(GyB_n*d);
p2_y(p2_y<1) = 1;
p2_y(p2_y>256) = 256;

%------------------------- question 8 -----------------------------

C = zeros(256);
% on enregistre dans le tableau les pixels appartenant a un contour 

for i = 1:256
    for j = 1:256
        if(GB(i,j)-GB(p1_x(i,j),p1_y(i,j)) > 0.5 && (GB(i,j)-GB(p2_x(i,j),p2_y(i,j)) > 0.5));
            C(i,j) = GB(i,j);
        end
    end
end

%------------------------- question 9 -----------------------------

figure(9)
imshow(C)
title('contour de l image bruitée');





