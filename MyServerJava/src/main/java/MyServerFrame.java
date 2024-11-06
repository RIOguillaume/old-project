import java.awt.Font;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.Socket;
import javax.swing.JFrame;


/**
 *
 * @author guill
 */
public class MyServerFrame extends JFrame {

    static Socket s;
    static ServerSocket ss;
    static InputStreamReader isr;
    static BufferedReader br;
    static String message;
    
    static double ax;
    static double ay;
    static double az;
    
    static double mx;
    static double my;
    static double mz;
    
    static double roll = 0;
    static double pitch = 0;
    static double yaw = 0;
    
    public MyServerFrame() {
        initComponents();
    }
   
    
    @SuppressWarnings("unchecked")
    // <editor-fold defaultstate="collapsed" desc="Generated Code">//GEN-BEGIN:initComponents
    private void initComponents() {

        jScrollPane1 = new javax.swing.JScrollPane();
        jTextArea1 = new javax.swing.JTextArea();

        setDefaultCloseOperation(javax.swing.WindowConstants.EXIT_ON_CLOSE);

        jTextArea1.setColumns(20);
        jTextArea1.setRows(5);
        jScrollPane1.setViewportView(jTextArea1);

        javax.swing.GroupLayout layout = new javax.swing.GroupLayout(getContentPane());
        getContentPane().setLayout(layout);
        layout.setHorizontalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(jScrollPane1, javax.swing.GroupLayout.DEFAULT_SIZE, 760, Short.MAX_VALUE)
                .addContainerGap())
        );
        layout.setVerticalGroup(
            layout.createParallelGroup(javax.swing.GroupLayout.Alignment.LEADING)
            .addGroup(layout.createSequentialGroup()
                .addContainerGap()
                .addComponent(jScrollPane1, javax.swing.GroupLayout.DEFAULT_SIZE, 633, Short.MAX_VALUE)
                .addContainerGap())
        );

        pack();
    }// </editor-fold>//GEN-END:initComponents
    
    private static void computeAccData(){
        message = message.replace(",", ".");

        String tmpS;
        int tmp = message.indexOf(":");
        message = message.substring(tmp + 1);

        //Ax
        int tmp1 = message.indexOf("/");
        tmpS = message.substring(0, tmp1);
        ax = Float.parseFloat(tmpS);
        message = message.substring(tmp1 + 1);

        //Ay
        tmp1 = message.indexOf("/");
        tmpS = message.substring(0, tmp1);
        ay = Float.parseFloat(tmpS);
        message = message.substring(tmp1 + 1);

        //Az
        az = Float.parseFloat(message);
    }
    
    private static void computeRollPitch(){ 
        double g = 9.82;
        if(ax>9.81){
            ax = 9.81;
        }else if(ax<-9.81){
            ax = -9.81;
        }
        pitch = Math.asin(ax/g);
        roll = Math.atan2(-ay,-az);
        
        if(ax<0&&az<0){
            pitch = -Math.PI - pitch;
        }else if (ax>0&&az<0){
            pitch = Math.PI - pitch;
        }  
    }
    
    private static void computeMagData() {
        message = message.replace(",", ".");

        String tmpS;
        int tmp = message.indexOf(":");
        message = message.substring(tmp + 1);

        //Ax
        int tmp1 = message.indexOf("/");
        tmpS = message.substring(0, tmp1);
        mx = Float.parseFloat(tmpS);
        message = message.substring(tmp1 + 1);

        //Ay
        tmp1 = message.indexOf("/");
        tmpS = message.substring(0, tmp1);
        my = Float.parseFloat(tmpS);
        message = message.substring(tmp1 + 1);

        //Az
        mz = Float.parseFloat(message);
        
    }

    private static void computeYaw() {
        double Ax = ax;
        double Ay = ay;
        double Az = az;

        //cross product of the magnetic field vector and the gravity vector
        double Hx = my * ax - mz * ay;
        double Hy = mz * ax - mx * ax;
        double Hz = mx * ay - my * ax;

        //normalize the values of resulting vector
        float invH = 1.0f / (float) Math.sqrt(Hx * Hx + Hy * Hy + Hz * Hz);
        Hx *= invH;
        Hy *= invH;
        Hz *= invH;

        //normalize the values of gravity vector
        float invA = 1.0f / (float) Math.sqrt(Ax * Ax + Ay * Ay + Az * Az);
        Ax *= invA;
        Az *= invA;

        //arctangent to obtain heading in radians
        yaw = Math.atan2(Hy, Az * Hx - Ax * Hz);
    }
    
    public static void main(String args[]) {
        /* Set the Nimbus look and feel */
        //<editor-fold defaultstate="collapsed" desc=" Look and feel setting code (optional) ">
        /* If Nimbus (introduced in Java SE 6) is not available, stay with the default look and feel.
         * For details see http://download.oracle.com/javase/tutorial/uiswing/lookandfeel/plaf.html 
         */
        try {
            for (javax.swing.UIManager.LookAndFeelInfo info : javax.swing.UIManager.getInstalledLookAndFeels()) {
                if ("Nimbus".equals(info.getName())) {
                    javax.swing.UIManager.setLookAndFeel(info.getClassName());
                    break;
                }
            }
        } catch (ClassNotFoundException | InstantiationException | IllegalAccessException | javax.swing.UnsupportedLookAndFeelException ex) {
            java.util.logging.Logger.getLogger(MyServerFrame.class.getName()).log(java.util.logging.Level.SEVERE, null, ex);
        }
        //</editor-fold>
        

        /* Create and display the form */
        java.awt.EventQueue.invokeLater(() -> {
            new MyServerFrame().setVisible(true);
        });
        
       
       
        try{
            ss = new ServerSocket(6000);
            //System.out.println(ss.getInetAddress());
            System.out.println(ss.getInetAddress().getLocalHost().getHostAddress());
            //System.out.println(ss.getLocalSocketAddress().toString());
            
            while(true){
                System.out.println("wait connection");
                s = ss.accept();
                isr = new InputStreamReader(s.getInputStream());
                br = new BufferedReader(isr);
                message = br.readLine();
                if(message.startsWith("a")){
                    computeAccData();
                    computeRollPitch();
                }else if(message.startsWith("m")){
                    computeMagData();
                    computeYaw();
                }
                message = String.format("Accelerometer data : \nroll : %.3f \npitch : %.3f \nyaw : %.3f ", Math.toDegrees(roll), Math.toDegrees(pitch), Math.toDegrees(yaw));
                if(Math.toDegrees(roll) >90 || Math.toDegrees(roll) < -90){
                    message += "\nEcran orienté vers le haut";
                }else{
                    message += "\nEcran orienté vers le sol";
                }
                try{
                    jTextArea1.setFont(new Font("Courier", Font.BOLD,45));
                    jTextArea1.setText(message);
                }catch(NullPointerException e){
                    
                }
                
            }
            
        }catch(IOException e){
            e.printStackTrace();
        }
        
    }
    

    // Variables declaration - do not modify//GEN-BEGIN:variables
    private javax.swing.JScrollPane jScrollPane1;
    private static javax.swing.JTextArea jTextArea1;
    // End of variables declaration//GEN-END:variables
}
