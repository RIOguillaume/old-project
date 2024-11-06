/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package tetris;
import java.awt.*;  
import javax.swing.JFrame;  

/**
 *
 * @author guill
 */
public class Ecran extends Canvas {
    Plateau plateau;
    Form form;
    int etageForm = 2;
    
    public Ecran(Plateau plateau){
        this.plateau = plateau;
    }
    public void nouvelleForm(){
        this.form = new Form();
    }
    
    public void paint(Graphics g) {  
        nouvelleForm();
        g.drawString("Hello",40,40);  
        setBackground(Color.WHITE); 
        for(int x=0;x<plateau.hauteur;x++){
            for(int y=0;y<plateau.largeur;y++){
                g.fillRect(30*x,30*y ,50, 50); 
            }
        }
        if(form != null){
            for(int x=0;x<=1;x++){
                for(int y=0;y<=2;y++){
                    if(form.form[x][y]==true){
                        g.setColor(Color.red);
                        g.fillRect(30*y,30*x +(etageForm*30) ,50, 50); 
                    }
                }
            }
        }
    }  
        
    
}
