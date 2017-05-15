<?php
        $uploaddir ='/var/www/html/upload/imagefile/';
        #echo $_POST[user_name];
        $uploadfile = $uploaddir.basename($_FILES['userfile']['name']);
        #echo $uploadfile;
        if(move_uploaded_file($_FILES['userfile']['tmp_name'], $uploadfile))
        {
                echo "upload succes\n";
        }else {
                echo "upload failed\n";
        }
        #echo "\n자세한 디버깅 정보입니다.:\n";
        #print_r($_FILES);
        //print_r($_FILES['userfile']['error']);        
        $command = escapeshellcmd('python3 /var/www/html/code/cnn/hsv_db.py '.$uploadfile);
        #echo $command;
        #echo "\n";
        $output = shell_exec($command);
                echo $output;
?>
