<?php

        // MySQL 서버 접근
        $mysqli = new mysqli("localhost","root","root","product");

        if($mysqli->connect_errno) {
                die('Connect Error : '.$mysqli->connect_error);
        }

        mysqli_set_charset($mysqli, "utf8");

        $index = 1;

        if($result = $mysqli->query('SELECT * FROM imvely')) {
                while($row = $result->fetch_object()) {
                        if($index == 21)
                                break;
                        echo $row->product_name.",,".$row->product_server_img_url."=";
                        $index ++;
                }
                $result->free();
        }
        $mysqli->close();

?>