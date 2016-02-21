<?php

include "flag.php";
?>

<!DOCTYPE html>
<html lang="en">
    <head>
        <title>Replace with Grace</title>
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
              <a class="navbar-brand" href="">Replace with Grace</a>
            </div>
            <div id="navbar" class="navbar-collapse collapse">
              <ul class="nav navbar-nav">
                <li class="active"><a href="">S&R</a></li>
              </ul>
            </div><!--/.nav-collapse -->
          </div>
        </nav>

        <div class="container">
            <div class="jumbotron">
                    <form onsubmit="senddata(); return false;">
                        <h2>Search & Replace</h2>
                        <label for="search" class="sr-only">/cow/</label>
                        <input type="text" name="search" id="search" class="form-control" placeholder="/cow/" required="" autofocus="">
                        <label for="replace" class="sr-only">cat</label>
                        <input type="text" name="replace" id="replace" class="form-control" placeholder="cat" required="" autofocus="">
                        <label for="content" class="sr-only">Content</label>
                        <textarea type="content" id="content" name="content" class="form-control" placeholder="cows are cute <3" required=""></textarea>
                        <br>
                        <button class="btn btn-lg btn-primary btn-block" type="submit">Do the work!</button>
                    </form>
                    <br>
                    <pre id="output">Output...</pre>
            </div>
        </div>


        <script src="assets/js/jquery-1.11.3.min.js"></script>
        <script src="assets/js/bootstrap.min.js"></script>
        <script src="assets/js/app.js"></script>
    </body>
</html>
