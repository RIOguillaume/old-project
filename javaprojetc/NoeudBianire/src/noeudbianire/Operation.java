/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package noeudbianire;

import java.util.HashMap;
import java.util.Map;

/**
 *
 * @author guill
 */
public class Operation {
    private String monOp;
    private Map<String,Operation> mesOp = new HashMap<>();
    
    public int evaluation(int nb1,int nb2){
        switch (monOp) {
            case "+":
                return nb1+nb2;
            case "-":
                return nb1-nb2;
            case "/":
                return nb1/nb2;
            case "*":
                return nb1*nb2;
            default:
                return -1;
                
        }
    }
    public static Operation getInstance(String monOpString){
        Operation op = new Operation();
        op.monOp = monOpString;
        op.mesOp.put(monOpString, op);
        return op;
    }
    private Operation(){
        
    }
    
    
    
}
