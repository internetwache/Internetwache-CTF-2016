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
                <li class="active"><a href="/index.php">Login</a></li>
                <li><a href="/register.php">Register</a></li>
                <li><a href="/logout.php">Logout</a></li>
              </ul>
            </div><!--/.nav-collapse -->
          </div>
        </nav>

        <div class="container">
            <div class="jumbotron">
                <?php
                    $logged_in = $_SESSION['loggedin'];

                    if(isset($_POST['user']) && isset($_POST['password'])) {
                        $user = $_POST['user'];
                        $password = md5($_POST['password']);

                        $q = mysqli_prepare($DBCON, "SELECT username FROM usertable where username = ? and pw = ? limit 1");
                        mysqli_stmt_bind_param($q, "ss", $user, $password);
                        mysqli_stmt_execute($q);
                        $res = mysqli_stmt_get_result($q);
                        if($res->num_rows > 0) {
                            $username = $res->fetch_array(MYSQLI_NUM)[0];

                            $q = mysqli_prepare($DBCON, "SELECT is_admin, comment FROM usertable where username = ? limit 1");
                            mysqli_stmt_bind_param($q, "s", $username);
                            mysqli_stmt_execute($q);
                            $res = mysqli_stmt_get_result($q);

                            $data = $res->fetch_array(MYSQLI_NUM);

                            $_SESSION['admin'] = $data[0];
                            $_SESSION['loggedin'] = true;
                            $_SESSION['comment'] = $data[1];

                            $q = mysqli_prepare($DBCON, "DELETE FROM usertable where is_admin = 0 and pw = ? limit 1");
                            mysqli_stmt_bind_param($q, "s", $password);
                            mysqli_stmt_execute($q);
                        }
                    }
                ?>

                <?php 
                if($_SESSION['loggedin']) {
                    echo '<h1>Welcome</h1>';
                    echo '<p>Here is your secret: '.($_SESSION['comment']).'</p>';
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
