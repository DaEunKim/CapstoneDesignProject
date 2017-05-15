package kookmin.cs.msdj.forstyle.Server;

import android.net.Uri;
import android.os.AsyncTask;
import android.util.Log;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.concurrent.ExecutionException;

/**
 * Created by dblab on 2017-04-04.
 */

public class EC2Server {
    private String urlPath;
    private final String uploadImagePath = "http://ec2-13-124-80-232.ap-northeast-2.compute.amazonaws.com/code/image/upload_image.php";
    private String user_name;
    private String imgName;
    private Uri uri;

    public static ArrayList<String> results;

    /* 사용자가 촬영한 사진을 서버로 전송하는 메소드 */
    public ArrayList<String> uploadPhoto(String user_name, Uri photouri, String img_Name) {
        this.user_name = user_name;
        this.imgName = img_Name;
        this.urlPath = uploadImagePath;
        this.uri = photouri;
        Log.d("EC2 Server ", imgName);
        try {
            results = new UploadImageTask().execute().get();
        } catch ( InterruptedException e ) {
            e.printStackTrace();
        } catch ( ExecutionException e ) {
            e.printStackTrace();
        }
        return results;
    }

    class UploadImageTask extends AsyncTask<Void, Void, ArrayList<String>> {
        @Override
        protected ArrayList<String> doInBackground(Void... voids) {
            // TODO Auto-generated method
            try {

                FileInputStream fileInputStream = new FileInputStream(imgName);
                URL url = new URL(urlPath); // Set url
                HttpURLConnection con = (HttpURLConnection) url.openConnection();
                con.setDoInput(true); // Available Write
                con.setDoOutput(true); // Available Read
                con.setUseCaches(false); // No cash
                con.setRequestMethod("POST");

                String boundary = "Specific String";
                con.setRequestProperty("Connection", "Keep-Alive");
                con.setRequestProperty("Content-Type", "multipart/form-data; boundary=" + boundary);


                // Open output stream
                DataOutputStream wr = new DataOutputStream(con.getOutputStream());

                wr.writeBytes("\r\n--" + boundary + "\r\n");

                wr.writeBytes("Content-Disposition:form-data;name=\"user_name\"\r\n\r\n"+user_name);

                wr.writeBytes("\r\n--" + boundary + "\r\n");

                wr.writeBytes("Content-Disposition:form-data;name=\"userfile\";filename=\"" + imgName + "\"\r\n");

                wr.writeBytes("Content-Type:application/octet-stream\r\n\r\n");


                int bytesAvailable = fileInputStream.available();
                int maxBufferSize = 1024;
                int bufferSize = Math.min(bytesAvailable, maxBufferSize);
                byte[] buffer = new byte[bufferSize];

                int bytesRead = fileInputStream.read(buffer, 0, bufferSize);
                while (bytesRead > 0) {
                    // Upload file part(s)
                    wr.write(buffer, 0, bufferSize);
                    bytesAvailable = fileInputStream.available();
                    bufferSize = Math.min(bytesAvailable, maxBufferSize);
                    bytesRead = fileInputStream.read(buffer, 0, bufferSize);
                    Log.e("uploadFile", "success");
                }

                wr.writeBytes("\r\n--" + boundary + "--\r\n");
                fileInputStream.close();
                wr.flush();
                wr.close();

                BufferedReader rd = null;
                rd = new BufferedReader(new InputStreamReader(con.getInputStream(),"UTF-8"));
                String line = null;
                ArrayList<String> qResults = new ArrayList<String>();
                while((line = rd.readLine()) != null) {
                    Log.d("BufferedReader:", line);
                    qResults.add(line);
                }
                return qResults;
            } catch (UnsupportedEncodingException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }
            return null;
        }
        protected void onPostExecute(ArrayList<String> qResults) {
            super.onPostExecute(qResults);
        }
    }
}
