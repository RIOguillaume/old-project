/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package tetris;

/**
 *
 * @author guill
 */
public class Plateau {
    boolean [][] plateau;
    int hauteur;
    int largeur;
    
    
    public Plateau(int hauteur,int largeur){
        this.plateau = new boolean[largeur][hauteur];
        this.largeur = largeur;
        this.hauteur = hauteur;   
    }
}
