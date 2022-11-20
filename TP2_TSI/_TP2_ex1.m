clear all; 
close all;

%% 1) Transformations d’histogramme

%------------------------- question 1 -----------------------------

figure(1)
Image = imread('pieces.png');
Image2= im2double(Image);
Affichage= imshow(Image2);
title('Image d origine');

%------------------------- question 2 -----------------------------

m1= rand(1); % atribution de valeur de m1 et m2 aléatoirement
m2= rand(1);

New_m1=m1; % définition des nouveux m1 et m2 qui vont varier 
New_m2=m2;

% compteur et somme servent à calculer les nouveaux m1 et m2

Label=zeros(221,261); % création de la matrice label de la taille de la matrice image 

while(1)    

    compteur_m_1=0; % création d'un compteur pour compter le nombre de 
    compteur_m_2=0; % valeur dans les labels 1 et 2

    somme_m_1=0; % variables qui servent à additionner les valeurs des 
    somme_m_2=0; % pixels allant dans les labels.

    m_1=New_m1; % définition des nouveux m_1 et m_2 qui servent uniquement 
    m_2=New_m2; % pour la boucle while prennent la valeur de New_m1/2
    
    for i = 1:221
        for j = 1:261
            
            a= abs(Image2(i,j)-m_1);
            b= abs(Image2(i,j)-m_2);
            
            if(b==min(a,b)); % si l'intensité du pixel est plus proche de m_2
            Label(i,j)=2; % on ajoute un 2 dans la matrice label aux coordonnées du pixel
            compteur_m_2=compteur_m_2+1; % on incémente le compteur
            somme_m_2=somme_m_2+Image2(i,j); % on ajoute la valeur du pixel à la somme 
                    
            elseif(a==min(a,b)); % de même avec intensité plus proche de m_1
            Label(i,j)=1;
            compteur_m_1=compteur_m_1+1;
            somme_m_1=somme_m_1+Image2(i,j);
            end
        end
    end
    
    New_m1=somme_m_1/compteur_m_1; % chgt des valeurs de New_m1/2 ce qui 
    New_m2=somme_m_2/compteur_m_2; % permet de continuer la boucle
    
    
  if (abs(New_m1-m_1))< 0.001 && (abs(New_m2-m_2)<0.001); % si New_m1/2 ne change pas 
      break; % on quitte la boucle while
  end
  
end


figure(2)
imshow(Label,[]);  
title('Image segmentée');


%------------------------- question 3 -----------------------------

[h,w]=size(Image2);

histo_image=imhist(Image2);
figure(3)
subplot(1,3,1)
bar(histo_image)
title('Histogramme de l image');

%------------------------- question 4 -----------------------------

[counts_image,X]=imhist(Image2);
histo_normalise=histo_image/(h*w);
subplot(1,3,2)
bar(histo_normalise)
title('Histogramme normalisé de l image');

%------------------------- question 5 -----------------------------

histo_cumule=cumsum(counts_image);
subplot(1,3,3)
plot(histo_cumule)
title('Histogramme cumulé de l image');

%------------------------- question 6 -----------------------------

Image_egalise=histeq(Image2,histo_cumule);
figure(4)
imshow(Image_egalise)
title('Image égalisé');

%------------------------- question 7 -----------------------------

[counts_egalise,histo_egalise]=imhist(Image_egalise);

figure(5)
bar(histo_egalise,counts_egalise/(h*w))
title('Histogramme de l image égalisé');

%------------------------- question 8 -----------------------------

[h_e,w_e]=size(Image_egalise);
[counts_image_egalise,histo_image_egalise]=imhist(Image_egalise);

figure(6)
subplot(1,3,1)
imshow(Image_egalise)
title('Image egalise');

histo_normalise_egalise=histo_image_egalise/(h*w);
subplot(1,3,2) 
bar(histo_normalise_egalise,counts_image_egalise/(h_e*w_e))
title('Histogramme normalisé de l image egalise');

histo_cumule_egalise=cumsum(counts_image_egalise);
subplot(1,3,3)
plot(histo_cumule_egalise)
title('Histogramme cumulé de l image egalise');


%------------------------- question 9 -----------------------------


% m1_e= 0.5529 + (1-0.5529)*rand(1); % on observe que sur l'image egalise l'intensité minimale est de "0.5529" et maximale "1" nous choissisons alors des valeur dans cette intervalle 
% m2_e= 0.5529 + (1-0.5529)*rand(1);

% m1_e = max(Image_egalise(:)) * rand(1,1);%valeur aleatoire entre 0 et 1
% m2_e = max(Image_egalise(:)) * rand(1,1);

m1_e=0.75;% on fixe deux valeur pour m1 et m2 
m2_e=0.85;

New_m1_e=m1_e; 
New_m2_e=m2_e;


Label_e=zeros(221,261); 

while(1)    

    compteur_m_1=0;  
    compteur_m_2=0; 

    somme_m_1=0;  
    somme_m_2=0; 

    m_1=New_m1_e;  
    m_2=New_m2_e;
    
    for i = 1:221
        for j = 1:261
            
            a= abs(Image_egalise(i,j)-m_1);
            b= abs(Image_egalise(i,j)-m_2);
            
            if(b==min(a,b)); 
            Label_e(i,j)=2; 
            compteur_m_2=compteur_m_2+1;
            somme_m_2=somme_m_2+Image_egalise(i,j);  
            
            
            
            elseif(a==min(a,b)); 
            Label_e(i,j)=1;
            compteur_m_1=compteur_m_1+1;
            somme_m_1=somme_m_1+Image_egalise(i,j);
            end
        end
    end
    
    New_m1_e=somme_m_1/compteur_m_1; 
    New_m2_e=somme_m_2/compteur_m_2; 
        
  if (abs(New_m1_e-m_1))<0.001 && (abs(New_m2_e-m_2)<0.001); 
      break; 
  end
  
end

figure(7)
imshow(Label_e,[]);  
title('Image égalisé segmentée');


%% 2) Morphologie mathématique : granulométrie


%------------------------- question 1 -----------------------------

figure(8)
subplot(1,3,1)
imshow(Label_e,[]);  
title('Image égalisé segmentée');

se=strel('disk',2);

Image_dilate=imdilate(Label_e,se);
subplot(1,3,2)
imshow(Image_dilate,[]);  
title('Image égalisée dilate');

Image_erode=imerode(Image_dilate,se);
subplot(1,3,3)
imshow(Image_erode,[])
title('Image égalisée amélioré');

%------------------------- question 2 -----------------------------

% c'est le marqueur ...

%------------------------- question 3 -----------------------------

New_image=imclearborder(Image_erode);
figure(9)
imshow(New_image)
title('Image bordures corrigées');

%------------------------- question 4 -----------------------------

Taille_objet=1:1:7;
nombre_objet= bweuler(New_image);
compteur=0;
objet=zeros(30,1);
j=2;
figure(10)

for i=1:1:30
    
    se=strel('sphere',i);
    Image_Finale=imopen(New_image,se);
    new_nombre_objet=bweuler(Image_Finale);
    difference_objet=nombre_objet-new_nombre_objet;
    subplot(1,4,1)
    imshow(New_image)
    title('image initiale');

    if (difference_objet ~= 0);
        objet(i)=difference_objet;
        nombre_objet=new_nombre_objet;
        
        subplot(1,4,j)
        imshow(Image_Finale)
        title('image nettoyée');
        j=j+1;
    end 
    
end

figure(11);
bar(objet,0.5);
title('Courbes Granulométrie');
xlabel('Taille élément structurant');
ylabel('Nombre de pieces retirées');

