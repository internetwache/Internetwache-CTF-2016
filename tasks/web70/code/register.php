<?php session_start(); ?>
<?php 
include "config.php";
?>
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>The adminpanel</title>
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
              <a class="navbar-brand" href="">The Secretstore</a>
            </div>
            <div id="navbar" class="navbar-collapse collapse">
              <ul class="nav navbar-nav">
                <li><a href="/index.php">Login</a></li>
                <li class="active"><a href="/register.php">Register</a></li>
                <li><a href="/logout.php">Logout</a></li>
              </ul>
            </div><!--/.nav-collapse -->
          </div>
        </nav>

        <div class="container">
            <div class="jumbotron">
                <?php
                    $logged_in = $_SESSION['loggedin'];

                    if($logged_in) {
                        echo '<h1>Error</h1>';
                        echo '<br><p>You are already registered. No need to register again.</p>';
                    } else {

                        if(isset($_POST['user']) && isset($_POST['password']) && isset($_POST['secret'])) {
                            $user = $_POST['user'];
                            $password = md5($_POST['password']);
                            $comment = $_POST['secret'];

                            $q = mysqli_prepare($DBCON, "SELECT id FROM usertable where username = ? limit 1");
                            mysqli_stmt_bind_param($q, "s", $user);
                            mysqli_stmt_execute($q);
                            $res = mysqli_stmt_get_result($q);
                            if ($res->num_rows > 0) {
                                echo '<h1>Error</h1>';
                                echo '<br><p>User already exists!</p>';
                            } else {
                                $zero = 0;
                                $q = mysqli_prepare($DBCON, "INSERT INTO usertable (username, pw, comment, is_admin) VALUES (?,?,?,?)");
                                mysqli_stmt_bind_param($q, "sssi", $user, $password, $comment, $zero);
                                $a = mysqli_stmt_execute($q);
                                if($a) {
                                    echo '<h1>YAY!</h1>';
                                    echo '<p>Kittens love you - You are now registered</p>';
                                } else {
                                    echo '<h1>Error:</h1>';
                                    echo '<p>Something went wrong</p>';
                                }
                            }
                        } 
                ?>

                    <form action="" method="POST" class="form-signin">
                        <h2>Create an account</h2>
                        <label for="user" class="sr-only">Username</label>
                        <input type="text" name="user" id="user" class="form-control" placeholder="Username" required="" autofocus="">
                        <label for="password" class="sr-only">Password</label>
                        <input type="password" id="password" name="password" class="form-control" placeholder="Password" required="">
                        <label for="secret" class="sr-only">Secret</label>
                        <input type="text" name="secret" id="secret" class="form-control" placeholder="Secret" required="" autofocus="">
                        <button class="btn btn-lg btn-primary btn-block" type="submit">Register</button>
                    </form>

                <?php
                    }
                ?>
            </div>
        </div>
        <script src="assets/js/jquery-1.11.3.min.js"></script>
        <script src="assets/js/bootstrap.min.js"></script>
    </body>
</html>
