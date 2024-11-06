package tetris;
import javax.swing.*; 
import java.awt.Color;  
import java.awt.Graphics;  
import java.util.concurrent.DelayQueue;
import javax.swing.JComponent;  
import javax.swing.JFrame;  

public class Tetris {  
    public static void main(String[] args) {  
        Ecran m = new Ecran(new Plateau(5,10));  
        JFrame f=new JFrame();  
        f.add(m);  
        f.setSize(400,400);  
        //f.setLayout(null);  
        f.setVisible(true);  
        while(true){
            m.etageForm = 3;
        }
    }  
    public void gestionClavier(){
        
    }
    
}  