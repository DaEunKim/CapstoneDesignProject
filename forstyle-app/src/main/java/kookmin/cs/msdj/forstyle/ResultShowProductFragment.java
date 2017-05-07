package kookmin.cs.msdj.forstyle;

import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.content.DialogInterface;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.drawable.BitmapDrawable;
import android.graphics.drawable.Drawable;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v4.app.Fragment;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.TextView;

import java.io.IOException;
import java.io.InputStream;
import java.io.UnsupportedEncodingException;
import java.lang.ref.WeakReference;
import java.lang.reflect.Array;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;

import kookmin.cs.msdj.forstyle.DB.DBManager;

/**
 * Created by dblab on 2017-03-18.
 */

public class ResultShowProductFragment extends Fragment implements View.OnClickListener {

    /* DB */
    private DBManager dbManager;
    private ArrayList<String> results;

    private int id_view;

    /* ImageView Component*/
    private ImageView iv_result_product1;
    private ImageView iv_result_product2;
    private ImageView iv_result_product3;
    private ImageView iv_result_product4;
    private ImageView iv_result_product5;
    private ImageView iv_result_product6;
    private ImageView iv_result_product7;
    private ImageView iv_result_product8;
    private ImageView iv_result_product9;
    private ImageView iv_result_product10;

    /* TextView Component */
    private TextView tv_result_product1;
    private TextView tv_result_product2;
    private TextView tv_result_product3;
    private TextView tv_result_product4;
    private TextView tv_result_product5;
    private TextView tv_result_product6;
    private TextView tv_result_product7;
    private TextView tv_result_product8;
    private TextView tv_result_product9;
    private TextView tv_result_product10;

    /* Button Component */
    private Button btn_search_next;
    private boolean is_clicked_next = true;

    /* String */
    private String product1_name;
    private String product2_name;
    private String product3_name;
    private String product4_name;
    private String product5_name;
    private String product6_name;
    private String product7_name;
    private String product8_name;
    private String product9_name;
    private String product10_name;
    private String product11_name;
    private String product12_name;
    private String product13_name;
    private String product14_name;
    private String product15_name;
    private String product16_name;
    private String product17_name;
    private String product18_name;
    private String product19_name;
    private String product20_name;

    private Bitmap bit;

    private String[] URLS;
    private String[] product_list;

    public static ArrayList<Drawable> drawables;
    private ProgressDialog mProgressDialog;


    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View rootView = inflater.inflate(R.layout.fragment_result_show_product, container, false);

        if(getArguments() != null) {
            product_list = getArguments().getStringArray("product_list");
        }

        dbManager = new DBManager();
        results = dbManager.selectProduct();
        URLS = new String[21];
        drawables = new ArrayList<Drawable>();

        /* Component */
        iv_result_product1 = (ImageView) rootView.findViewById(R.id.iv_result_product1);
        iv_result_product2 = (ImageView) rootView.findViewById(R.id.iv_result_product2);
        iv_result_product3 = (ImageView) rootView.findViewById(R.id.iv_result_product3);
        iv_result_product4 = (ImageView) rootView.findViewById(R.id.iv_result_product4);
        iv_result_product5 = (ImageView) rootView.findViewById(R.id.iv_result_product5);
        iv_result_product6 = (ImageView) rootView.findViewById(R.id.iv_result_product6);
        iv_result_product7 = (ImageView) rootView.findViewById(R.id.iv_result_product7);
        iv_result_product8 = (ImageView) rootView.findViewById(R.id.iv_result_product8);
        iv_result_product9 = (ImageView) rootView.findViewById(R.id.iv_result_product9);
        iv_result_product10 = (ImageView) rootView.findViewById(R.id.iv_result_product10);

        tv_result_product1 = (TextView) rootView.findViewById(R.id.tv_result_product_1);
        tv_result_product2 = (TextView) rootView.findViewById(R.id.tv_result_product_2);
        tv_result_product3 = (TextView) rootView.findViewById(R.id.tv_result_product_3);
        tv_result_product4 = (TextView) rootView.findViewById(R.id.tv_result_product_4);
        tv_result_product5 = (TextView) rootView.findViewById(R.id.tv_result_product_5);
        tv_result_product6 = (TextView) rootView.findViewById(R.id.tv_result_product_6);
        tv_result_product7 = (TextView) rootView.findViewById(R.id.tv_result_product_7);
        tv_result_product8 = (TextView) rootView.findViewById(R.id.tv_result_product_8);
        tv_result_product9 = (TextView) rootView.findViewById(R.id.tv_result_product_9);
        tv_result_product10 = (TextView) rootView.findViewById(R.id.tv_result_product_10);

        btn_search_next = (Button) rootView.findViewById(R.id.btn_search_next);

        /* Click Listener */
        iv_result_product1.setOnClickListener(this);
        iv_result_product2.setOnClickListener(this);
        iv_result_product3.setOnClickListener(this);
        iv_result_product4.setOnClickListener(this);
        iv_result_product5.setOnClickListener(this);
        iv_result_product6.setOnClickListener(this);
        iv_result_product7.setOnClickListener(this);
        iv_result_product8.setOnClickListener(this);
        iv_result_product9.setOnClickListener(this);
        iv_result_product10.setOnClickListener(this);
        tv_result_product1.setOnClickListener(this);
        tv_result_product2.setOnClickListener(this);
        tv_result_product3.setOnClickListener(this);
        tv_result_product4.setOnClickListener(this);
        tv_result_product5.setOnClickListener(this);
        tv_result_product6.setOnClickListener(this);
        tv_result_product7.setOnClickListener(this);
        tv_result_product8.setOnClickListener(this);
        tv_result_product9.setOnClickListener(this);
        tv_result_product10.setOnClickListener(this);
        btn_search_next.setOnClickListener(this);

        updateUI(results);

        return rootView;
    }

    public void updateUI(ArrayList<String> results) {
        String[] result_query = results.get(0).split("=");
        String[] result_product1 = result_query[0].split(",,");
        String[] result_product2 = result_query[1].split(",,");
        String[] result_product3 = result_query[2].split(",,");
        String[] result_product4 = result_query[3].split(",,");
        String[] result_product5 = result_query[4].split(",,");
        String[] result_product6 = result_query[5].split(",,");
        String[] result_product7 = result_query[6].split(",,");
        String[] result_product8 = result_query[7].split(",,");
        String[] result_product9 = result_query[8].split(",,");
        String[] result_product10 = result_query[9].split(",,");
        String[] result_product11 = result_query[10].split(",,");
        String[] result_product12 = result_query[11].split(",,");
        String[] result_product13 = result_query[12].split(",,");
        String[] result_product14 = result_query[13].split(",,");
        String[] result_product15 = result_query[14].split(",,");
        String[] result_product16 = result_query[15].split(",,");
        String[] result_product17 = result_query[16].split(",,");
        String[] result_product18 = result_query[17].split(",,");
        String[] result_product19 = result_query[18].split(",,");
        String[] result_product20 = result_query[19].split(",,");

        product1_name = "H&M"+product_list[0];
        product2_name = "H&M"+product_list[1];
        product3_name = "H&M"+product_list[2];
        product4_name = "H&M"+product_list[3];
        product5_name = "H&M"+product_list[4];
        product6_name = "H&M"+product_list[5];
        product7_name = "H&M"+product_list[6];
        product8_name = "H&M"+product_list[7];
        product9_name = "H&M"+product_list[8];
        product10_name = "H&M"+product_list[9];
        product11_name = "H&M"+product_list[10];
        product12_name = "H&M"+product_list[11];
        product13_name = "H&M"+product_list[12];
        product14_name = "H&M"+product_list[13];
        product15_name = "H&M"+product_list[14];
        product16_name = "H&M"+product_list[15];
        product17_name = "H&M"+product_list[16];
        product18_name = "H&M"+product_list[17];
        product19_name = "H&M"+product_list[18];
        product20_name = "H&M"+product_list[19];
        /*
        product1_name = result_product1[0];
        product2_name = result_product2[0];
        product3_name = result_product3[0];
        product4_name = result_product4[0];
        product5_name = result_product5[0];
        product6_name = result_product6[0];
        product7_name = result_product7[0];
        product8_name = result_product8[0];
        product9_name = result_product9[0];
        product10_name = result_product10[0];
        product11_name = result_product11[0];
        product12_name = result_product12[0];
        product13_name = result_product13[0];
        product14_name = result_product14[0];
        product15_name = result_product15[0];
        product16_name = result_product16[0];
        product17_name = result_product17[0];
        product18_name = result_product18[0];
        product19_name = result_product19[0];
        product20_name = result_product20[0];
        */

        URLS[0] = new String("");
        URLS[1] = new String(DBManager.ec2ImageUrlPath+product_list[0]+".jpg");
        URLS[2] = new String(DBManager.ec2ImageUrlPath+product_list[1]+".jpg");
        URLS[3] = new String(DBManager.ec2ImageUrlPath+product_list[2]+".jpg");
        URLS[4] = new String(DBManager.ec2ImageUrlPath+product_list[3]+".jpg");
        URLS[5] = new String(DBManager.ec2ImageUrlPath+product_list[4]+".jpg");
        URLS[6] = new String(DBManager.ec2ImageUrlPath+product_list[5]+".jpg");
        URLS[7] = new String(DBManager.ec2ImageUrlPath+product_list[6]+".jpg");
        URLS[8] = new String(DBManager.ec2ImageUrlPath+product_list[7]+".jpg");
        URLS[9] = new String(DBManager.ec2ImageUrlPath+product_list[8]+".jpg");
        URLS[10] = new String(DBManager.ec2ImageUrlPath+product_list[9]+".jpg");
        URLS[11] = new String(DBManager.ec2ImageUrlPath+product_list[10]+".jpg");
        URLS[12] = new String(DBManager.ec2ImageUrlPath+product_list[11]+".jpg");
        URLS[13] = new String(DBManager.ec2ImageUrlPath+product_list[12]+".jpg");
        URLS[14] = new String(DBManager.ec2ImageUrlPath+product_list[13]+".jpg");
        URLS[15] = new String(DBManager.ec2ImageUrlPath+product_list[14]+".jpg");
        URLS[16] = new String(DBManager.ec2ImageUrlPath+product_list[15]+".jpg");
        URLS[17] = new String(DBManager.ec2ImageUrlPath+product_list[16]+".jpg");
        URLS[18] = new String(DBManager.ec2ImageUrlPath+product_list[17]+".jpg");
        URLS[19] = new String(DBManager.ec2ImageUrlPath+product_list[18]+".jpg");
        URLS[20] = new String(DBManager.ec2ImageUrlPath+product_list[19]+".jpg");

        tv_result_product1.setText(product1_name);
        tv_result_product2.setText(product2_name);
        tv_result_product3.setText(product3_name);
        tv_result_product4.setText(product4_name);
        tv_result_product5.setText(product5_name);
        tv_result_product6.setText(product6_name);
        tv_result_product7.setText(product7_name);
        tv_result_product8.setText(product8_name);
        tv_result_product9.setText(product9_name);
        tv_result_product10.setText(product10_name);

        WebGetImage task = new WebGetImage();
        task.execute(1);
    }

    @Override
    public void onClick(View v) {
        id_view = v.getId();
        if (id_view == R.id.iv_result_product1 || id_view == R.id.tv_result_product_1)
            ;
        else if (id_view == R.id.iv_result_product2 || id_view == R.id.tv_result_product_2)
            ;
        else if (id_view == R.id.iv_result_product3 || id_view == R.id.tv_result_product_3)
            ;
        else if (id_view == R.id.iv_result_product4 || id_view == R.id.tv_result_product_4)
            ;
        else if (id_view == R.id.iv_result_product5 || id_view == R.id.tv_result_product_5)
            ;
        else if (id_view == R.id.iv_result_product6 || id_view == R.id.tv_result_product_6)
            ;
        else if (id_view == R.id.iv_result_product7 || id_view == R.id.tv_result_product_7)
            ;
        else if (id_view == R.id.iv_result_product8 || id_view == R.id.tv_result_product_8)
            ;
        else if (id_view == R.id.iv_result_product9 || id_view == R.id.tv_result_product_9)
            ;
        else if (id_view == R.id.iv_result_product10 || id_view == R.id.tv_result_product_10)
            ;
        else if(id_view == R.id.btn_search_next) {
            is_clicked_next = !is_clicked_next;
            if(is_clicked_next == false) {
                btn_search_next.setText("previous");
                WebGetImage task = new WebGetImage();
                task.execute(11);
                tv_result_product1.setText(product11_name);
                tv_result_product2.setText(product12_name);
                tv_result_product3.setText(product13_name);
                tv_result_product4.setText(product14_name);
                tv_result_product5.setText(product15_name);
                tv_result_product6.setText(product16_name);
                tv_result_product7.setText(product17_name);
                tv_result_product8.setText(product18_name);
                tv_result_product9.setText(product19_name);
                tv_result_product10.setText(product20_name);
            }else {
                btn_search_next.setText("next");
                WebGetImage task = new WebGetImage();
                task.execute(1);
                tv_result_product1.setText(product1_name);
                tv_result_product2.setText(product2_name);
                tv_result_product3.setText(product3_name);
                tv_result_product4.setText(product4_name);
                tv_result_product5.setText(product5_name);
                tv_result_product6.setText(product6_name);
                tv_result_product7.setText(product7_name);
                tv_result_product8.setText(product8_name);
                tv_result_product9.setText(product9_name);
                tv_result_product10.setText(product10_name);
            }

        }
    }

    // 네트워크에 접속하여 이미지를 가져오는 클래스 선언
    class WebGetImage extends AsyncTask<Integer, Integer, Bitmap> {

        int index_start;

        @Override
        protected void onPreExecute() {
            super.onPreExecute();
            mProgressDialog = new ProgressDialog(getActivity());
            mProgressDialog.setMessage(getString(R.string.loading));
            mProgressDialog.setIndeterminate(true);
            mProgressDialog.show();
        }

        @Override
        protected Bitmap doInBackground(Integer... params) {
            // 네트워크에 접속해서 데이터를 가져옴

            try {
                //웹사이트에 접속 (사진이 있는 주소로 접근)
                index_start = params[0];
                URL Url;
                for (int i = index_start; i < index_start+10; i++) {
                    Url = new URL(URLS[i]);
                    Log.d("ResultShowFragment","URL:"+URLS[i]);
                    // 웹사이트에 접속 설정
                    HttpURLConnection conn = (HttpURLConnection) Url.openConnection();
                    conn.setDoInput(true);
                    // 연결하시오
                    conn.connect();
                    // 스트림 클래스를 이용하여 이미지를 불러옴
                    InputStream is = conn.getInputStream();
                    // 스트림을 통하여 저장된 이미지를 이미지 객체에 넣어줌
                    bit = BitmapFactory.decodeStream(is);

                    drawables.add(new BitmapDrawable(bit));
                }

            } catch (UnsupportedEncodingException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }
            return bit;
        }

        protected void onPostExecute(Bitmap bit) {
            iv_result_product1.setBackground(drawables.get(index_start-1));
            iv_result_product2.setBackground(drawables.get(index_start));
            iv_result_product3.setBackground(drawables.get(index_start+1));
            iv_result_product4.setBackground(drawables.get(index_start+2));
            iv_result_product5.setBackground(drawables.get(index_start+3));
            iv_result_product6.setBackground(drawables.get(index_start+4));
            iv_result_product7.setBackground(drawables.get(index_start+5));
            iv_result_product8.setBackground(drawables.get(index_start+6));
            iv_result_product9.setBackground(drawables.get(index_start+7));
            iv_result_product10.setBackground(drawables.get(index_start+8));
            mProgressDialog.dismiss();
        }
    }
}