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
                <li><a href="/register.php">Register</a></li>
                <li class="active"><a href="/logout.php">Logout</a></li>
              </ul>
            </div><!--/.nav-collapse -->
          </div>
        </nav>

        <div class="container">
            <div class="jumbotron">
                <?php
                    unset($_SESSION['loggedin']);
                    session_destroy();
                ?>
                <h1>Good bye!</h1>
                <br>
                <a href="/index.php">Login again</a>
            </div>
        </div>
        <script src="assets/js/jquery-1.11.3.min.js"></script>
        <script src="assets/js/bootstrap.min.js"></script>
    </body>
</html>
