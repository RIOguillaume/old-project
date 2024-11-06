/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package noeudbianire;

/**
 *
 * @author guill
 */
public class NoeudValeur implements Noeud{
    private int valeur;
    public NoeudValeur (int valeur){
        this.valeur = valeur;
    }
    @Override
    public int evaluation(){
        return valeur;
    }
    
}
