<?php

include "flag.php";
include "bf-protection.php";

$admin_user = "pr0_adm1n";
$admin_pw = clean_hash("0e408306536730731920197920342119"); //Super uncrackable hash, eh?

function clean_hash($hash) {
    return preg_replace("/[^0-9a-f]/","",$hash);
}

//Comparison of short hashes is very very efficient. At least that's what my students say...
function myhash($str) {
    return clean_hash(md5(md5($str) . "SALT"));
}

if(is_bf($_SERVER['REMOTE_ADDR'])) {
    die("THINK before anything! Try again in 1 second.");
}
?>

<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Mess of Hash</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="assets/css/bootstrap.min.css" />
        <link rel="stylesheet" href="assets/css/style.css" />
    </head>
    <body>
        <nav class="navbar navbar-default navbar-fixed-top">
          <div class="container">
            <div class="navbar-header">
              <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
              </button>
              <a class="navbar-brand" href="">Mess of Hash</a>
            </div>
            <div id="navbar" class="navbar-collapse collapse">
              <ul class="nav navbar-nav">
                <li class="active"><a href="">Login</a></li>
              </ul>
            </div><!--/.nav-collapse -->
          </div>
        </nav>

        <div class="container">
            <div class="jumbotron">
                <?php
                    $logged_in = false;
                    if(isset($_POST['user']) && isset($_POST['password'])) {
                        if($_POST['user'] == $admin_user) {
                            if(myhash($_POST['password']) == $admin_pw) {
                                $logged_in = true;
                            } else {
                                echo 'try harder ;)';
                            }
                        } else {
                            echo 'try harder ;)';
                        }
                    }
                ?>

                <?php 
                if($logged_in) {
                    echo "<p>$FLAG</p>";
                } else {
                ?>
                    <form action="" method="POST" class="form-signin">
                        <h2>Please login</h2>
                        <label for="user" class="sr-only">Username</label>
                        <input type="text" name="user" id="user" class="form-control" placeholder="Username" required="" autofocus="">
                        <label for="password" class="sr-only">Password</label>
                        <input type="password" id="password" name="password" class="form-control" placeholder="Password" required="">
                        <button class="btn btn-lg btn-primary btn-block" type="submit">Sign in</button>
                    </form>
                <?php } ?>
            </div>
        </div>
        <script src="assets/js/jquery-1.11.3.min.js"></script>
        <script src="assets/js/bootstrap.min.js"></script>
    </body>
</html>
