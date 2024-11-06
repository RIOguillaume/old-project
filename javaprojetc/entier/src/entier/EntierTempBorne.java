/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package entier;

import java.util.Observable;

/**
 *
 * @author guill
 */
public class EntierTempBorne extends Entier{
    private static int nbMsgEnregister = 0;
    private int nbMsgAvantDefaite = 3;
    private Entier monJeuEntier;
    private String msgTempBorne;
    
    public EntierTempBorne() {
        monJeuEntier = new Entier();
    }
    
    public void changerDifficulte (int difficulte){
        nbMsgAvantDefaite = difficulte;
    }
    @Override
    public void tester(int nbChoisi){
        if (nbMsgEnregister < nbMsgAvantDefaite){
            nbMsgEnregister++;
            monJeuEntier.tester(nbChoisi);
            msgTempBorne = monJeuEntier.getMsg();
        }else {
            msgTempBorne = "Vous avez perdu car vous avez dépassé le nombre d'éssais autorisé.";
        } 
    }
    @Override
    public String getMsg(){
        return msgTempBorne;
    }
    
    
}
