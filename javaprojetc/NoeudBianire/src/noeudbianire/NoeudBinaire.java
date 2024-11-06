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
public class NoeudBinaire implements Noeud{
    Noeud composant1;
    Noeud composant2;
    Operation monOp;
    
    public NoeudBinaire(Noeud nb1,Noeud nb2, Operation ope){
        this.composant1 = nb1;
        this.composant2 = nb2;
        this.monOp = ope;
    }
    private NoeudBinaire(){
        
    }
    @Override
    public int evaluation(){
        return monOp.evaluation(composant1.evaluation(), composant2.evaluation());
    }
    
}
