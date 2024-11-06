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
public class Form {
    boolean[][] form = new boolean[2][3];
    public Form(){
        form = generationFormAle();
    }
    boolean[][] generationFormAle(){
        boolean[][] bar = new boolean[2][3];
        bar[0][0] = true;
        bar[0][1] = true;
        bar[0][2] = true;
        boolean[][] bloc = new boolean[2][3];
        bloc[0][0] = true;
        bloc[0][1] = true;
        bloc[1][0] = true;
        bloc[1][1] = true;
        boolean[][] Te = new boolean[2][3];
        Te[0][0] = true;
        Te[0][1] = true;
        Te[0][2] = true;
        Te[1][1] = true;
        boolean[][] L = new boolean[2][3];
        L[0][0] = true;
        L[0][1] = true;
        L[0][2] = true;
        L[1][0] = true;
        boolean[][] J = new boolean[2][3];
        J[0][0] = true;
        J[0][1] = true;
        J[0][2] = true;
        J[1][2] = true;
        boolean[][] Z = new boolean[2][3];
        Z[0][0] = true;
        Z[0][1] = true;
        Z[1][1] = true;
        Z[1][2] = true;
        boolean[][] S = new boolean[2][3];
        S[1][0] = true;
        S[1][1] = true;
        S[0][1] = true;
        S[0][2] = true;
        switch((int)(Math.random()*6)){
            case 0:
                return bloc;
            case 1:
                return bar;
            case 2:
                return Te;
            case 3:
                return L;
            case 4:
                return J;
            case 5:
                return Z;
            case 6:
                return S;
        }
        return bar;
    }
}
