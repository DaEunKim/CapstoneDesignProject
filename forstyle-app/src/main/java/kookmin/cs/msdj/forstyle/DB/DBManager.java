package kookmin.cs.msdj.forstyle.DB;

import android.os.AsyncTask;
import android.util.Log;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.concurrent.ExecutionException;

/**
 * Created by dblab on 2017-03-18.
 */

public class DBManager {
    private String urlPath;
    public static final String ec2ImageUrlPath = "http://ec2-13-124-80-232.ap-northeast-2.compute.amazonaws.com/topten/image_";
    private final String selectProductPath = "http://ec2-13-124-80-232.ap-northeast-2.compute.amazonaws.com/code/mysql/select_product.php";

    /* Product Data */
    private String product_name;
    private String product_cost;
    private String product_server_img_url;
    private String shopping_url;

    public static ArrayList<String> results;

    /* 상품 조회 부분 */
    public ArrayList<String> selectProduct() {
        urlPath = selectProductPath;
        try {
            results = new InquiryUser().execute().get();
        } catch ( InterruptedException e ) {
            e.printStackTrace();
        } catch ( ExecutionException e ) {
            e.printStackTrace();
        }
        return results;
    }

    class InquiryUser extends AsyncTask<Void, Void, ArrayList<String>> {
        @Override
        protected ArrayList<String> doInBackground(Void... voids) {
            // TODO Auto-generated method
            try {
                URL url = new URL(urlPath); // Set url
                HttpURLConnection con = (HttpURLConnection) url.openConnection();
                con.setDoInput(true); // Available Write
                con.setDoOutput(true); // Available Read
                con.setUseCaches(false); // No cash
                con.setRequestMethod("POST");
                /*
                String param = "user_id="+user_id+"&user_password="+user_password;
                OutputStream outputStream = con.getOutputStream();
                outputStream.write(param.getBytes());
                outputStream.flush();
                outputStream.close();
                */

                BufferedReader rd = null;
                ArrayList<String> qResults = new ArrayList<String>();

                rd = new BufferedReader(new InputStreamReader(con.getInputStream(),"UTF-8"));
                String line = "";
                while((line = rd.readLine()) != null) {
                    Log.d("BufferedReader:", line);
                    if(line != null) {
                        qResults.add(line);
                    }
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
