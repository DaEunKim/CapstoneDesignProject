package kookmin.cs.msdj.forstyle;

import android.*;
import android.Manifest;
import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Bundle;
import android.os.Environment;
import android.os.Handler;
import android.provider.MediaStore;
import android.renderscript.ScriptGroup;
import android.support.annotation.NonNull;
import android.support.annotation.Nullable;
import android.support.v4.app.ActivityCompat;
import android.support.v4.app.Fragment;
import android.support.v4.app.FragmentTransaction;
import android.support.v4.content.ContextCompat;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Toast;

import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.text.SimpleDateFormat;
import java.util.ArrayList;

import kookmin.cs.msdj.forstyle.Server.EC2Server;

import static android.app.Activity.RESULT_OK;

/**
 * Created by dblab on 2017-03-07.
 */

public class SearchImageFragment extends Fragment implements View.OnClickListener{

    private EC2Server server;

    // Request Code
    private static final int PICK_FROM_CAMERA = 0;
    private static final int PICK_FROM_ALBUM = 1;
    private static final int CROP_FROM_IMAGE = 2;

    // Fragment component
    private Button btn_search_photo;
    private Button btn_search_next;

    private ImageView iv_search_image;

    private int id_view;
    private Uri mImageCaptureUri;
    private String absoultePath;
    private String strPhotoName;

    private ProgressDialog mProgressDialog;
    private Handler handler;

    public static ArrayList<String> results;

    @Nullable
    @Override
    public View onCreateView(LayoutInflater inflater, @Nullable ViewGroup container, @Nullable Bundle savedInstanceState) {
        View rootView = inflater.inflate(R.layout.fragment_search_image, container, false);

        /* EC2 Server */
        server = new EC2Server();

        /* Component */
        btn_search_photo = (Button) rootView.findViewById(R.id.btn_search_photo);
        btn_search_next = (Button) rootView.findViewById(R.id.btn_search_next);
        iv_search_image = (ImageView) rootView.findViewById(R.id.search_image);

        results = new ArrayList<String>();

        /* Click Listener */
        btn_search_photo.setOnClickListener(this);
        btn_search_next.setOnClickListener(this);

        return rootView;
    }

    public void grantUriPermission(){
        // 갤러리 사용 권한 체크
        if(ContextCompat.checkSelfPermission(getActivity(), Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED) {
            // 최초 권한 요청인지 혹은 사용자에게 의한 재요청인지 확인
            if(ActivityCompat.shouldShowRequestPermissionRationale(getActivity(), Manifest.permission.WRITE_EXTERNAL_STORAGE)) {
                // 사용자가 임의로 권한을 취소 시킨 경우, 권한 재요청
                ActivityCompat.requestPermissions(getActivity(), new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, 1);
            } else {
                ActivityCompat.requestPermissions(getActivity(), new String[]{Manifest.permission.WRITE_EXTERNAL_STORAGE}, 1);
            }
        }else if(ContextCompat.checkSelfPermission(getActivity(), Manifest.permission.READ_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED) {
            // 최초 권한 요청인지 혹은 사용자에게 의한 재요청인지 확인
            if(ActivityCompat.shouldShowRequestPermissionRationale(getActivity(), Manifest.permission.READ_EXTERNAL_STORAGE)) {
                // 사용자가 임의로 권한을 취소 시킨 경우, 권한 재요청
                ActivityCompat.requestPermissions(getActivity(), new String[]{Manifest.permission.READ_EXTERNAL_STORAGE}, 1);
            } else {
                ActivityCompat.requestPermissions(getActivity(), new String[]{Manifest.permission.READ_EXTERNAL_STORAGE}, 1);
            }
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, @NonNull String[] permissions, @NonNull int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        switch(requestCode) {
            case 1: {
                if (grantResults.length > 0 && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    return;
                }else {
                    Toast.makeText(getActivity(), "권한 사용을 동의해주셔야 이용 가능합니다.", Toast.LENGTH_LONG).show();
                }
                return;
            }
        }
    }


    @Override
    public void onClick(View v) {
        id_view = v.getId();
        if(id_view == R.id.btn_search_photo) {

            DialogInterface.OnClickListener cameraListener = new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                    doTakePhotoAction();
                }
            };
            DialogInterface.OnClickListener albumListener = new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                    doTakeAlbumAction();
                }
            };

            DialogInterface.OnClickListener cancelListener = new DialogInterface.OnClickListener() {
                @Override
                public void onClick(DialogInterface dialog, int which) {
                    dialog.dismiss();
                }
            };

            new AlertDialog.Builder(getActivity())
                    .setTitle("업로드할 이미지 선택")
                    .setPositiveButton("사진촬영", cameraListener)
                    .setNeutralButton("앨범선택", albumListener)
                    .setNegativeButton("취소", cancelListener)
                    .show();
        }else if(id_view == R.id.btn_search_next) {
            Log.d("SearchImageFragment", "uri "+mImageCaptureUri.getPath().toString());
            Log.d("SearchImageFragment", "absolute path "+absoultePath);
            results = server.uploadPhoto("kjc",mImageCaptureUri, absoultePath);
            int size = results.size();
            String product = results.get(size-2).toString();
            product = product.replaceAll("\\[","");
            product = product.replaceAll("\\]","");
            product = product.replaceAll(" ","");
            String[] product_list = product.split(",");
            //Log.d("SearchImageFragment","product size : "+size);

            ResultShowProductFragment fragment = new ResultShowProductFragment();

            Bundle bundle = new Bundle();
            bundle.putStringArray("product_list", product_list);
            fragment.setArguments(bundle);

            FragmentTransaction ft = getActivity().getSupportFragmentManager().beginTransaction();
            ft.add(R.id.content_fragment_layout, fragment);
            ft.replace(R.id.content_fragment_layout, fragment);
            ft.commit();
        }
    }

    /**
     * 카메라에서 사진 촬영
     */
    public void doTakePhotoAction() // 카메라 촬영 후 이미지 가져오기
    {
        Log.d("SearchImageFragment","doTakePhotoAction");
        Intent intent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);

        // 임시로 사용할 파일의 경로를 생성
        String url = "tmp_" + String.valueOf(System.currentTimeMillis()) + ".jpg";
        mImageCaptureUri = Uri.fromFile(new File(Environment.getExternalStorageDirectory(), url));

        intent.putExtra(MediaStore.EXTRA_OUTPUT, mImageCaptureUri);
        startActivityForResult(intent, PICK_FROM_CAMERA);
    }

    /**
     * 앨범에서 이미지 가져오기
     */
    public void doTakeAlbumAction() // 앨범에서 이미지 가져오기
    {
        // 앨범 호출
        Log.d("SearchImageFragment","doTakeAlbumAction");
        Intent intent = new Intent(Intent.ACTION_PICK);
        intent.setType(MediaStore.Images.Media.CONTENT_TYPE);
        startActivityForResult(intent, PICK_FROM_ALBUM);
    }

    @Override
    public void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);
        Log.d("SearchImageFragment","onActivityResult");
        if (resultCode != RESULT_OK)
            return;
        Log.d("SearchImageFragment","requestCode");
        switch (requestCode) {

            case PICK_FROM_ALBUM: {
                // 이후의 처리가 카메라와 같으므로 일단  break없이 진행합니다.
                // 실제 코드에서는 좀더 합리적인 방법을 선택하시기 바랍니다.
                mImageCaptureUri = data.getData();

                File original_file = getImageFile(mImageCaptureUri);
                mImageCaptureUri = createSaveCropFile();

                File copy_file = new File(mImageCaptureUri.getPath());
                Log.d("SearchImageFragment", mImageCaptureUri.getPath().toString());
                copyCropFile(original_file, copy_file);

                //Intent intent = new Intent("com.android.camera.action.CROP");
                //intent.setDataAndType(mImageCaptureUri, "image/*");
                //intent.putExtra(MediaStore.EXTRA_OUTPUT, mImageCaptureUri);

            }

            case PICK_FROM_CAMERA: {
                // 이미지를 가져온 이후의 리사이즈할 이미지 크기를 결정합니다.
                // 이후에 이미지 크롭 어플리케이션을 호출하게 됩니다.
                Intent intent = new Intent("com.android.camera.action.CROP");
                intent.setDataAndType(mImageCaptureUri, "image/*");
                intent.putExtra("output", mImageCaptureUri);
                startActivityForResult(intent, CROP_FROM_IMAGE); // CROP_FROM_CAMERA case문 이동
                break;
            }
            case CROP_FROM_IMAGE: {
                // 크롭이 된 이후의 이미지를 넘겨 받습니다.
                // 이미지뷰에 이미지를 보여준다거나 부가적인 작업 이후에
                // 임시 파일을 삭제합니다.
                if (resultCode != getActivity().RESULT_OK) {
                    return;
                }

                String img_path = mImageCaptureUri.getPath();
                Bitmap bmp = BitmapFactory.decodeFile(img_path);
                iv_search_image.setImageBitmap(bmp);

                SimpleDateFormat timeFormat = new SimpleDateFormat("yyyymmdd_hhmmss");
                String curTime = timeFormat.format(System.currentTimeMillis());
                String filePath = Environment.getExternalStorageDirectory().getAbsolutePath()+
                        "/ForStyle/"+curTime+".jpg";

                storeCropImage(bmp, filePath);
                //final Bundle extras = data.getExtras();
                absoultePath = filePath;
                /*
                if (extras != null) {
                    Bitmap photo = extras.getParcelable("data"); // CROP된 BITMAP
                    // Bitmap.createScaledBitmap() 메소드를 통해 비트맵 이미지를 64*64로 리사이즈한다.
                    //  64*64는 하드웨어 길이에 적용한 사이즈이다.
                    //Bitmap resize_photo = Bitmap.createScaledBitmap(photo, 64, 64, true);

                    iv_search_image.setImageBitmap(photo); // 레이아웃의 이미지칸에 CROP된 BITMAP을 보여줌

                    storeCropImage(photo, filePath); // CROP된 이미지를 외부저장소, 앨범에 저장한다.


                    break;

                }*/

                // 임시 파일 삭제
                File f = new File(mImageCaptureUri.getPath());
                if (f.exists()) {
                    f.delete();
                }
            }
        }
    }

    /*
     * Bitmap을 저장하는 부분
     */
    private void storeCropImage(Bitmap bitmap, String filePath) {
        // ForStyel 폴더를 생성하여 이미지를 저장하는 방식이다.
        String dirPath = Environment.getExternalStorageDirectory().getAbsolutePath()+"/ForStyle";
        File directory_ForStyle = new File(dirPath);

        if(!directory_ForStyle.exists()) // SmartWheel 디렉터리에 폴더가 없다면 (새로 이미지를 저장할 경우에 속한다.)
            directory_ForStyle.mkdir();

        File copyFile = new File(filePath);
        BufferedOutputStream out = null;

        try {
            copyFile.createNewFile();
            out = new BufferedOutputStream(new FileOutputStream(copyFile));
            bitmap.compress(Bitmap.CompressFormat.JPEG, 100, out);

            // sendBroadcast를 통해 Crop된 사진을 앨범에 보이도록 갱신한다.
            getActivity().sendBroadcast(new Intent(Intent.ACTION_MEDIA_SCANNER_SCAN_FILE,
                    Uri.fromFile(copyFile)));

            out.flush();
            out.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    /**
     * @author : pppdw
     * @param : Crop된 이미지가 저장될 파일을 만든다.선언된 url로 파일이 네이밍되며, 선언된 uri에 파일이 저장된다.
     * @return : Uri
     */
    private Uri createSaveCropFile(){
        Uri uri;
        SimpleDateFormat timeFormat = new SimpleDateFormat("yyyymmdd_hhmmss");
        String curTime = timeFormat.format(System.currentTimeMillis());
        String url = curTime+".jpg";
        //String url = "" + String.valueOf(System.currentTimeMillis()) + ".jpg";
        strPhotoName = url;

        // ForStyle 폴더를 생성하여 이미지를 저장하는 방식이다.
        String dirPath = Environment.getExternalStorageDirectory().getAbsolutePath()+"/ForStyle";
        File directory_ForStyle = new File(dirPath);

        if(!directory_ForStyle.exists()) // SmartWheel 디렉터리에 폴더가 없다면 (새로 이미지를 저장할 경우에 속한다.)
            directory_ForStyle.mkdir();

        uri = Uri.fromFile(new File(dirPath, url));
        return uri;
    }

    private File getImageFile(Uri uri) {
        String[] projection = { MediaStore.Images.Media.DATA };
        if (uri == null) {
            uri = MediaStore.Images.Media.EXTERNAL_CONTENT_URI;
        }
        grantUriPermission();
        Cursor mCursor = getActivity().getContentResolver().query(uri, projection, null, null,
                MediaStore.Images.Media.DATE_MODIFIED + " desc");
        if(mCursor == null || mCursor.getCount() < 1) {
            return null; // no cursor or no record
        }
        int column_index = mCursor.getColumnIndexOrThrow(MediaStore.Images.Media.DATA);
        mCursor.moveToFirst();

        String path = mCursor.getString(column_index);

        if (mCursor !=null ) {
            mCursor.close();
            mCursor = null;
        }

        return new File(path);
    }

    /**
     * @author pppdw
     * @description 크롭을 위해 사진을 복사한다.
     * @return
     */

    public static boolean copyCropFile(File srcFile, File destFile) {
        boolean result = false;
        try {
            InputStream in = new FileInputStream(srcFile);
            try {
                result = copyToFile(in, destFile);
            } finally {
                in.close();
            }
        } catch (IOException e) {
            result = false;
        }
        return result;
    }

    /**
     * @author : pppdw
     * @description : DestFile을 소스스트림에 복사한다 (데이터밸류)
     */
    private static boolean copyToFile(InputStream inputStream, File destFile) {
        try {
            OutputStream out = new FileOutputStream(destFile);
            try {
                byte[] buffer = new byte[4096];
                int bytesRead;
                while ((bytesRead = inputStream.read(buffer)) >= 0) {
                    out.write(buffer, 0, bytesRead);
                }
            } finally {
                out.close();
            }
            return true;
        } catch (IOException e) {
            return false;
        }
    }
    // 프로그레스바를 설정한다.
    private void showProgressDialog() {
        if (mProgressDialog == null) {
            mProgressDialog = new ProgressDialog(getActivity());
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
