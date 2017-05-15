package kookmin.cs.msdj.forstyle;

import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.AsyncTask;
import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentTransaction;
import android.util.Log;
import android.view.View;
import android.support.design.widget.NavigationView;
import android.support.v4.view.GravityCompat;
import android.support.v4.widget.DrawerLayout;
import android.support.v7.app.ActionBarDrawerToggle;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.ImageView;
import android.widget.TextView;

import com.google.android.gms.auth.api.Auth;
import com.google.android.gms.auth.api.signin.GoogleSignInOptions;
import com.google.android.gms.auth.api.signin.GoogleSignInResult;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.common.api.OptionalPendingResult;

import java.io.IOException;
import java.io.InputStream;
import java.io.UnsupportedEncodingException;
import java.net.HttpURLConnection;
import java.net.URL;

public class MainActivity extends AppCompatActivity
        implements NavigationView.OnNavigationItemSelectedListener {

    private static final String TAG = "MainActivity";
    private GoogleSignInOptions gso;
    private GoogleApiClient mGoogleApiClient;
    private GoogleSignInResult result;

    // SharedPreference
    private SharedPreferences prefs;

    // Navi_veiw
    private View nav_view;

    // Navi-Component
    private ImageView personPhoto;
    private TextView personName;
    private TextView personEmail;

    //
    private Bitmap bit;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        ActionBarDrawerToggle toggle = new ActionBarDrawerToggle(
                this, drawer, toolbar, R.string.navigation_drawer_open, R.string.navigation_drawer_close);
        drawer.setDrawerListener(toggle);
        toggle.syncState();

        NavigationView navigationView = (NavigationView) findViewById(R.id.nav_view);
        navigationView.setNavigationItemSelectedListener(this);

        nav_view = navigationView.getHeaderView(0);
        personPhoto = (ImageView) nav_view.findViewById(R.id.personPhoto);
        personName = (TextView) nav_view.findViewById(R.id.personName);
        personEmail = (TextView) nav_view.findViewById(R.id.personEmail);

        setNaviDrawerGooglePersonSync();

        FragmentTransaction ft = getSupportFragmentManager().beginTransaction();
        ft.replace(R.id.content_fragment_layout, new SearchImageFragment());
        ft.commit();
    }

    @Override
    public void onBackPressed() {
        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        if (drawer.isDrawerOpen(GravityCompat.START)) {
            drawer.closeDrawer(GravityCompat.START);
        } else {
            super.onBackPressed();
        }
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }

    @SuppressWarnings("StatementWithEmptyBody")
    @Override
    public boolean onNavigationItemSelected(MenuItem item) {
        // Handle navigation view item clicks here.
        int id = item.getItemId();
        Fragment fragment = null; // 메뉴에 따라 이동할 Fragment

        if (id == R.id.nav_camera) {
            fragment = new SearchImageFragment();
            Log.d("MainActivity","SearchImageFragment");
        } else if (id == R.id.nav_gallery) {
            fragment = new ResultShowProductFragment();
            Log.d("MainActivity","ResultShowProductFragment");
        } else if (id == R.id.nav_slideshow) {
        } else if (id == R.id.nav_manage) {

        } else if (id == R.id.nav_share) {

        } else if (id == R.id.nav_send) {

        }

        if(fragment != null) {
            FragmentTransaction ft = getSupportFragmentManager().beginTransaction();
            ft.replace(R.id.content_fragment_layout, fragment);
            ft.commit();
        }

        DrawerLayout drawer = (DrawerLayout) findViewById(R.id.drawer_layout);
        drawer.closeDrawer(GravityCompat.START);

        return true;
    }

    public void setNaviDrawerGooglePersonSync() {
        prefs = getSharedPreferences("GOOGLE_LOGIN",0); // SharedPreference 환경 변수 사용
        String email = prefs.getString("PERSON_EMAIL","None");
        String name = prefs.getString("PERSON_NAME","None");
        String photo_uri = prefs.getString("PERSON_PHOTO_URI","None");
        personEmail.setText(email);
        personName.setText(name);
        WebGetImage task = new WebGetImage();
        task.execute(photo_uri);
    }

    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        Log.d("MainActivity","onActivityResult");
        Fragment f = new SearchImageFragment();
        f.onActivityResult(requestCode,resultCode,data);
    }

    // 네트워크에 접속하여 이미지를 가져오는 클래스 선언
    class WebGetImage extends AsyncTask<String, Integer, Bitmap> {

        @Override
        protected Bitmap doInBackground(String... urls) {
            // 네트워크에 접속해서 데이터를 가져옴

            try {
                //웹사이트에 접속 (사진이 있는 주소로 접근)
                URL Url = new URL(urls[0]);
                // 웹사이트에 접속 설정
                HttpURLConnection conn = (HttpURLConnection)Url.openConnection();
                conn.setDoInput(true);
                // 연결하시오
                conn.connect();
                // 스트림 클래스를 이용하여 이미지를 불러옴
                InputStream is = conn.getInputStream();
                // 스트림을 통하여 저장된 이미지를 이미지 객체에 넣어줌
                bit = BitmapFactory.decodeStream(is);

            } catch (UnsupportedEncodingException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }
            return bit;
        }


        protected void onPostExecute (Bitmap bit) {
            personPhoto.setImageBitmap(bit);
        }

    }
}
