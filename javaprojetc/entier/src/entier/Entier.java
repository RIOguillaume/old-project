/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package entier;

/**
 *
 * @author guill
 */
public class Entier {
    private int nb;
    private String msg = "";
    
    public Entier(){
        nb = (int)(Math.random());
    }
    
    public void tester(int nbChoisi){
        if (nb == nbChoisi){
            msg = "Vous avez gagné !";
        } else {
            msg = "Vous avez perdu retentez votre chance.";
        }
    }
    public String getMsg(){
        return msg;
    }
    
    
    public static void main(String[] args) {
        Entier monjeu = new EntierTempBorne();
        monjeu.tester(5);
        monjeu.tester(5);
        monjeu.tester(5);
        
        System.out.println(monjeu.getMsg());
    }
    
}
