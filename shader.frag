#version 330 core

// Variable d'entrée
in vec3 coordonnee_3d;

uniform vec4 c;

// Variable de sortie (sera utilisé comme couleur)
out vec4 color;

//Un Fragment Shader minimaliste
void main (void)
{
  //Couleur du fragment
  color = c;
  
  float r = c[0]+coordonnee_3d[0] ;
  float g = c[1]+coordonnee_3d[1] ;
  float b = c[2]+coordonnee_3d[2] ;

  color = vec4(r,g,b,0.0);
    
    
}
