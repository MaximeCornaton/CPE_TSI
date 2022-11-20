clear all; close all;

%% 4) Filtrage à partir d’histogramme : seuillage par K-means

%------------------------- question 1 -----------------------------

figure(1)
Image = imread('flower.png');
Image2= im2double(Image);
Affichage= imshow(Image2);
title('Image d origine');

%------------------------- question 2 -----------------------------

m1= rand(1); % atribution de valeur de m1 et m2 aléatoirement
m2= rand(1);

New_m1=m1; % définition des nouveux m1 et m2 qui vont varier 
New_m2=m2;

% compteur et somme servent à calculer les nouveaux m1 et m2

Label=zeros(256); % création de la matrice label de la taille de la matrice image 

while(1)    

    compteur_m_1=0; % création d'un compteur pour compter le nombre de 
    compteur_m_2=0; % valeur dans les labels 1 et 2

    somme_m_1=0; % variables qui servent à additionner les valeurs des 
    somme_m_2=0; % pixels allant dans les labels.

    m_1=New_m1; % définition des nouveux m_1 et m_2 qui servent uniquement 
    m_2=New_m2; % pour la boucle while prennent la valeur de New_m1/2
    
    for i = 1:256
        for j = 1:256
            
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

%------------------------- question 3 -----------------------------

figure(2)
imshow(Label,[]);  
title('Image segmentée');
