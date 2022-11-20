clear all; close all;

%% 2) Filtrage passe-haut dans l’espace de Fourier

n=2;
fc=3;

%------------------------- question 1 -----------------------------

figure(1)
voieLacte = imread('ngc2175.png');
Image= im2double(voieLacte);
Affichage= imshow(Image);
title('Image d origine');

%------------------------- question 2 -----------------------------
[h,w]=size(Image);
[U,V] = meshgrid(-w/2+1/2:w/2-1/2,-h/2+1/2:h/2-1/2);

D=sqrt(U.^2 +V.^2);

H = 1./(1+(fc./D).^2*n);

figure(2);
plot3(U,V,H)
title('Filtre de Butterworth en 3D');
%------------------------- question 3 -----------------------------

FFT_Image=fft2(Image);
FFT_Image2=fftshift(FFT_Image);

figure(3)
imagesc(log10(1+abs(FFT_Image2)))
title('Module de la transformée de Fourier de l image');
colormap('gray');
%------------------------- question 4 -----------------------------

New_Image=H.*FFT_Image2;

figure(4)
imagesc(log10(1+abs(New_Image)))
title('Module de la transformée de Fourier de l image avec filtre');
colormap('gray');

%------------------------- question 5 -----------------------------

New_Image2=ifftshift(New_Image);
Image_Finale=ifft2(New_Image2);
figure(5) 
imshow(Image_Finale)
title('Image Filtré');



