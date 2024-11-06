package com.example.senddatatopc;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Matrix;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorEventListener;
import android.hardware.SensorManager;
import android.os.AsyncTask;
import android.os.Bundle;
import android.os.StrictMode;
import android.view.View;
import android.widget.EditText;
import android.widget.Button;
import android.widget.TextView;

import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;

public class MainActivity extends AppCompatActivity implements SensorEventListener,View.OnClickListener {

    private EditText e1;
    private Button button;


    private SensorManager sensorManager;
    private Sensor magnetometer;
    private Sensor accelerometer;
    private boolean lastAccelerometerSet = false;
    private boolean lastMagnetometerSet = false;
    private float[] lastAccelerometer = new float[3];
    private float[] lastMagnetometer = new float[3];

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);


        e1 = (EditText) findViewById(R.id.editText);
        button= (Button)findViewById(R.id.button);
        button.setOnClickListener(this);
        StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
        StrictMode.setThreadPolicy(policy);

        sensorManager = (SensorManager) getSystemService(Context.SENSOR_SERVICE);
        magnetometer = sensorManager.getDefaultSensor(Sensor.TYPE_MAGNETIC_FIELD);
        accelerometer = sensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);


    }
    @Override
    protected void onResume() {
        super.onResume();
        sensorManager.registerListener(this, magnetometer, SensorManager.SENSOR_DELAY_GAME);
        sensorManager.registerListener(this, accelerometer, SensorManager.SENSOR_DELAY_GAME);
    }

    @Override
    protected void onPause() {
        super.onPause();
        sensorManager.unregisterListener(this, magnetometer);
        sensorManager.unregisterListener(this, accelerometer);
    }

    @Override
    public void onSensorChanged(SensorEvent event) {
        if (event.sensor == magnetometer) {
            System.arraycopy(event.values, 0, lastMagnetometer, 0, event.values.length);
            send_data("m:"+String.format("%.2f",event.values[0])+ " / " + String.format("%.2f", event.values[1]) + " / " +String.format("%.2f", event.values[2]));
        } else if (event.sensor == accelerometer) {
            System.arraycopy(event.values, 0, lastAccelerometer, 0, event.values.length);
            System.out.println("a:" + String.format("%.2f", event.values[0]) + " / " + String.format("%.2f", event.values[1]) + " / " + String.format("%.2f", event.values[2]));
            send_data("a:" + String.format("%.2f", event.values[0]) + " / " + String.format("%.2f", event.values[1]) + " / " + String.format("%.2f", event.values[2]));
        }
    }

    @Override
    public void onAccuracyChanged(Sensor sensor, int accuracy) {

    }

    public void send_data(){
        String message = e1.getText().toString();
        BackgroundTask b1 = new BackgroundTask();
        b1.doInBackground(message);

    }
    public void send_data(String message){
        BackgroundTask b1 = new BackgroundTask();
        b1.doInBackground(message);

    }

    @Override
    public void onClick(View view) {
        send_data();
    }

    class BackgroundTask extends AsyncTask<String,Void,Void>{
        private Socket s;
        private PrintWriter writer;

        @Override
        protected Void doInBackground(String... voids) {
            try{
                String message = voids[0];
                System.out.println(message);

                s = new Socket("192.168.191.104",6000);
                writer = new PrintWriter(s.getOutputStream());
                writer.write(message);
                writer.flush();
                writer.close();
            }catch (IOException e){
                e.printStackTrace();
            }
            return null;
        }
    }

}