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
public class Main {

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        NoeudValeur n1 = new NoeudValeur(10);
        NoeudValeur n2 = new NoeudValeur(5);
        
        NoeudBinaire monOp = new NoeudBinaire(n1,n2 , Operation.getInstance("*"));
        System.out.println(monOp.evaluation());
    }
    
}
