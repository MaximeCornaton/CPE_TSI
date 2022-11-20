clear all;
close all;
%% Question 1 :

%Affichage image
figure(1);
imageini = imread('pieces.png');%lire l'image
imageini2 = im2double(imageini);
imshow(imageini2);%afficher l'image
title('Image ');

%% Question 2 :

m1 = max(imageini2(:)) * rand(1,1);%valeur aleatoire entre 0 et 1
m2 = max(imageini2(:)) * rand(1,1);


nouveau_m1=m1;
nouveau_m2=m2;

%compteurs comptant le nb de valeurs proches de m1 et de m2
cpt1 = 0;
cpt2 = 0;

%somme des valeurs des pixels proches de m1 et de m2
somme1 = 0;
somme2 = 0;

label=zeros(221,261);

while(1)
    m12 = nouveau_m1;
    m22 = nouveau_m2;
    
    for i =1:221 %parcourt des ligne
        for j=1:261 %parcourt des colonnes
            x = abs(imageini2(i,j) -m12);
            y = abs(imageini2(i,j) - m22);
            if(x == min(x,y))
                label(i,j)=1;
                cpt1 = cpt1 +1;
                somme1 = imageini2(i,j) + somme1;
            elseif(y == min(x,y))
                label(i,j)=2;
                cpt2 = cpt2+1;
                somme2 = imageini2(i,j) + somme2;
            end
        end
    end
    nouveau_m1 = somme1/cpt1;
    nouveau_m2 = somme2/cpt2;
    
    
    if (abs(nouveau_m1 - m12))<0.01 && (abs(nouveau_m2 - m22))<0.01%si nouveau_m1 = m12 (resp m2) cela signifie qu'on a termine de parcourir l'image
        break;
    end
end

figure(2);
imshow(label, []);
title('image segmentee avec l algorithme K-mean ');

%% question3
figure(3)
[H,X] = imhist(imageini2);
bar(X, H);
title('Histogramme');
xlabel('intensite');
ylabel('nombre de pixels');
%% Question 4 
h = 221;
w = 261;
figure(4)
[H_norm] = H./(h*w);
bar(X, H_norm);
title('Histogramme normalise');
xlabel('intensite');
ylabel('nombre de pixels');

%% Question 5 
figure(5)
hold on;
H_cum = cumsum(H_norm);
plot(X,H_cum);
bar(X, H_norm);
title('Histogramme cumulé');
xlabel('intensite');
ylabel('nombre de pixels');


%% Question 6 
for i = 1: 221;
    for j = 1:261;
               
       im_eg(i,j) = H_cum(imageini(i,j)+1);
    end
end
%% Question 7
[H_eg, X_eg]=imhist(im_eg);
figure(6)
bar(X_eg, H_eg./(h*w));
title('Histogramme egalise');

%% Question 8
figure(7)
subplot(311)
imshow(im_eg);%afficher l'image
title('Image egalisee');
subplot(312)
bar(X, H_norm);
title('histogramme normalise');
xlim([0 1]);
subplot(313)
plot(X,H_cum);
title('Histogramme cumulé');

%% Question 9
m1 = max(im_eg(:)) * rand(1,1);%valeur aleatoire entre 0 et 1
m2 = max(im_eg(:)) * rand(1,1);

m3 = max(m1,m2);
nouveau_m1=min(m1,m2);
nouveau_m2=m3;

%compteurs comptant le nb de valeurs proches de m1 et de m2
cpt1 = 1;
cpt2 = 1;

%somme des valeurs des pixels proches de m1 et de m2
somme1 = 1;
somme2 = 1;

label=zeros(221,261);

while(1)
    m12 = nouveau_m1;
    m22 = nouveau_m2;
    
    for i =1:221 %parcourt des ligne
        for j=1:261 %parcourt des colonnes
            x = abs(im_eg(i,j) -m12);
            y = abs(im_eg(i,j) - m22);
            if(x == min(x,y))
                label(i,j)=1;
                cpt1 = cpt1 +1;
                somme1 = im_eg(i,j) + somme1;
            elseif(y == min(x,y))
                label(i,j)=2;
                cpt2 = cpt2+1;
                somme2 = im_eg(i,j) + somme2;
            end
        end
    end
    nouveau_m1 = somme1/cpt1;
    nouveau_m2 = somme2/cpt2;
    
    
    if (abs(nouveau_m1 - m12))<0.01 && (abs(nouveau_m2 - m22))<0.01%si nouveau_m1 = m12 (resp m2) cela signifie qu'on a termine de parcourir l'image
        break;
    end
end

figure(8);
imshow(label, []);
title('image segmentee de l image egalisee avec l algorithme K-mean ');

%% PARTIE 2
%% Question1
SE = strel('disk',3); %creation de l element structurant
im_dilate = imdilate(imcomplement(label-1), SE);
figure(9)
imshow(im_dilate);
title('image dilatee');
im_ferm = imerode(im_dilate, SE);
figure(10)
imshow(im_ferm);
title('image ayant subie une fermeture (dilatation puis erosion)');

%% Question 3

im_bord = imclearborder(im_ferm);
figure(11)
imshow(im_bord);
title('image ayant subie une fermeture dont les bords ont ete supprime')

% %% Question 4
% bw = bweuler(im_bord);
% figure(12)
% granu = zeros(7,1);
% i=1;
% for j=21:27 %rayon des cercles
%     subplot(3,4,i);
%     SE = strel('disk',j);
%     image = imopen(im_bord,SE);
%     imshow(image)
%     title(['image pour un ES = ', num2str(j)]);
%     granu(i,1)=bweuler(image);
%     i = i+1;
% end
% granu2 = granu;
% for i= 2:7
%     courbe(i,1) = granu2(i-1,1) - granu(i,1);
% end
% granu(1,1)=0;
% figure(13)
% stem(21:27,courbe);
% title('courbe de granulation');
% xlabel('rayons');
% ylabel('nombre de piece');

%% Question bonus
marqueur = zeros(221,261);
marqueur(9,111) = 1;
marqueur(221,104) = 1;
marqueur(107,206 ) = 1;
SE = strel('disk',3);
marqueur_dila = zeros(221,261);

 while(max(max(abs(marqueur_dila - marqueur))) ~= 0)
     marqueur_dila = marqueur;
     marqueur_dila = imdilate(marqueur_dila, SE);
     marqueur_dila = marqueur_dila .*im_ferm;
 end
 figure(14)
 imshow(marqueur_dila);

