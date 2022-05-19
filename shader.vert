#version 330 core

uniform vec4 translation;

// Variable d'entrée, ici la position
layout (location = 0) in vec3 position;

//Un Vertex Shader minimaliste
void main (void)
{
  //Coordonnees du sommet
     gl_Position=vec4(position, 1.0)+translation;
}
