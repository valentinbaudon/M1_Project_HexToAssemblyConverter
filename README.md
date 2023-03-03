
# Projet M1
### Traducteur de fichier hexa bruts provenant de microcontrôleurs basés sur une architecture ARM vers leur code assembleur

Cette application est un moyen de convertir des fichiers hexadécimaux en leur code assembleur.

Le fonctionnement de l'application est simple :

    1) Cliquez sur le bouton 'Download Hex File' pour télécharger le fichier héxadecimal que vous souhaitez traduire. Le contenu de votre fichier original devrait s'afficher dans le carré de texte comportant l'en-tete 'Hexadécimal'
    2) Selectionnez l'option d'affichage qui vous convient
    Plusieurs options d'affichage sont disponibles:
        - Compact : instruction et valeurs
        - Classique : instruction détaillée et valeurs
        - Intégral : valeur binaire correspondante à l'instruction, instruction détaillée et valeurs

    3) Cliquez sur le bouton 'Convertir'. Le contenu de votre fichier original traduit en assembleur devrait s'afficher dans le carré de texte comportant l'en-tete 'Assembleur'

    Si l'affichage obtenu ne vous convient pas, sélectionnez votre nouvelle option d'affichage et cliquez de nouveau sur le bouton 'Convertir'. Le nouveau contenu obtenu devrait remplacer l'ancien résultat.

    4) Pour télécharger ce visuel ou vous voulez sur votre ordinateur, cliquez sur le bouton 'Download Assembly File'
    
    Exemple d'affichage selon les options selectionnées
        - Compact: 0x08000003 : LSR (immediate) : R7, R3, #28
        - Classic: 0x08000003 : Logical Shift Right (Immediate) : R7, R3, #28
        - Integral: 0x08000003 : 0000111100011111 : Logical Shift Right (Immediate) : R7, R3, #28

Projet réalisé par Valentin BAUDON et Hugo MERLE, sous la direction de M. Jean-Jacques MENEU
