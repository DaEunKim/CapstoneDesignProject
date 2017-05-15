package kookmin.cs.msdj.forstyle;

import android.app.ProgressDialog;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Bundle;
import android.support.annotation.NonNull;

import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.View;

import com.google.android.gms.auth.api.Auth;
import com.google.android.gms.auth.api.signin.GoogleSignInAccount;
import com.google.android.gms.auth.api.signin.GoogleSignInOptions;
import com.google.android.gms.auth.api.signin.GoogleSignInResult;
import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.SignInButton;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.common.api.OptionalPendingResult;
import com.google.android.gms.common.api.ResultCallback;

public class LoginActivity extends AppCompatActivity implements
        GoogleApiClient.OnConnectionFailedListener, View.OnClickListener{

    private static final String TAG = "LoginActivity";
    private GoogleSignInOptions gso;
    private GoogleApiClient mGoogleApiClient;
    private GoogleSignInResult result;

    private SharedPreferences prefs;

    private ProgressDialog mProgressDialog;
    private static final int RC_SIGN_IN = 9001;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_login);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        // Button listener
        findViewById(R.id.sign_in_button).setOnClickListener(this);

        /* Google Sign-In 은 유저의 아이디와 기본적인 프로필 정보를 요청하도록 개체를 만든다.
        사용자의 전자 메일 주소도 요청하려면 requsetEmail() 를 호출한다. */
        // [START configure_signin]
        // Configure sign-in to request the user's ID, email address, and basic
        // profile. ID and basic profile are included in DEFAULT_SIGN_IN.
        gso = new GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN).requestEmail().build();
        // [END configure_signin]

        // [START build_client]
        // Build a GoogleApiClient with access to the Google Sign-In API and the
        // options specified by gso.
        mGoogleApiClient = new GoogleApiClient.Builder(this)
                .enableAutoManage(this /* FragmentActivity */, this /* OnConnectionFailedListener */)
                .addApi(Auth.GOOGLE_SIGN_IN_API, gso)
                .build();
        // [END build_client]

        // Set the dimensions of the sign-in button.
        SignInButton signInButton = (SignInButton) findViewById(R.id.sign_in_button);
        // [END customize_button]
    }

    // [START onStart]
    @Override
    protected void onStart() {
        super.onStart();
        // 구글의 로그인 결과를 확인한다.
        OptionalPendingResult<GoogleSignInResult> opr = Auth.GoogleSignInApi.silentSignIn(mGoogleApiClient);
        if(opr.isDone()) { // 사용자의 저장된 정보가 유효하다면 Done.
            // If the user's cached credentials are valid, the OptionalPendingResult will be "done"
            // and the GoogleSignInResult will be available instantly.
            result = opr.get();
            handleSignInResult(result); // 로그인을 처리하는 함수로 구글 로그인 결과를 전달한다.
        }else{
            // If the user has not previously signed in on this device or the sign-in has expired,
            // this asynchronous branch will attempt to sign in the user silently.  Cross-device
            // single sign-on will occur in this branch.
            showProgressDialog();
            opr.setResultCallback(new ResultCallback<GoogleSignInResult>() {
                @Override
                public void onResult(@NonNull GoogleSignInResult googleSignInResult) {
                    hideProgressDialog();
                    handleSignInResult(googleSignInResult);
                }
            });
        }
    }
    // [END onStart]

    // [START onActivityResult]
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        // Result returned from launching the Intent from GoogleSignInApi.getSignInIntent(...);
        if (requestCode == RC_SIGN_IN) {
            GoogleSignInResult result = Auth.GoogleSignInApi.getSignInResultFromIntent(data);
            handleSignInResult(result);
        }
    }

    // [START handleSignInResult]
    private void handleSignInResult(GoogleSignInResult result) {
        Log.d(TAG, "handleSignInResult:" + result.isSuccess());
        if (result.isSuccess()) { // 로그인 결과가 성공했따면
            saverPrefsGooglePersonData(result);
            startActivity(new Intent(LoginActivity.this, MainActivity.class)); // MainActivity를 실행한다.
        }
    }
    // [END handleSignInResult]

    // 구글 로그인을 한 사용자의 정보를 환경변수에 저장한다.
    public void saverPrefsGooglePersonData(GoogleSignInResult result) {
        if(result.isSuccess()) {
            GoogleSignInAccount acct = result.getSignInAccount(); // Google Login한 사용자의 정보를 가져온다.
            prefs = getSharedPreferences("GOOGLE_LOGIN", 0); // SharedPreference 환경 변수 사용
            SharedPreferences.Editor editor = prefs.edit();
            editor.putString("PERSON_NAME", acct.getDisplayName());
            editor.putString("PERSON_EMAIL", acct.getEmail());
            Log.d(TAG, "이름 : " + acct.getDisplayName() + " 이메일 주소 : " + acct.getEmail());
            if(acct.getPhotoUrl() != null) {
                editor.putString("PERSON_PHOTO_URI", acct.getPhotoUrl().toString());
                Log.d(TAG, "사용자 이미지 : " + acct.getPhotoUrl().toString());
            } else
                editor.putString("PERSON_PHOTO_URI", "null");

            editor.commit();
        }
    }

    @Override
    public void onClick(View v) {
        if(v.getId() == R.id.sign_in_button) {
            Intent signInIntent
                    = Auth.GoogleSignInApi.getSignInIntent(mGoogleApiClient);
            startActivityForResult(signInIntent, RC_SIGN_IN);
        }

    }

    @Override
    public void onConnectionFailed(@NonNull ConnectionResult connectionResult) {
        Log.d(TAG, "onConnectionFailed : "+connectionResult);
    }

    // 프로그레스바를 설정한다.
    private void showProgressDialog() {
        if (mProgressDialog == null) {
            mProgressDialog = new ProgressDialog(this);
            mProgressDialog.setMessage(getString(R.string.loading));
            mProgressDialog.setIndeterminate(true);
        }
        mProgressDialog.show();
    }

    // 프로그레스바를 숨긴다.
    private void hideProgressDialog() {
        if (mProgressDialog != null && mProgressDialog.isShowing()) {
            mProgressDialog.hide();
        }
    }
}
