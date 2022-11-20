#version 330 core

// Variable d'entrée, ici la position
layout (location = 0) in vec3 position;

uniform vec4 translation;
uniform mat4 rotation;
uniform mat4 projection;

// Variable de sortie
out vec3 coordonnee_3d;

//Un Vertex Shader minimaliste
void main (void)
{
    coordonnee_3d = position ;

    //Coordonnees du sommet
    gl_Position =   (vec4(position, 1.0) * rotation) ;
    gl_Position = gl_Position + translation ;
    gl_Position = projection * gl_Position ;
}
 