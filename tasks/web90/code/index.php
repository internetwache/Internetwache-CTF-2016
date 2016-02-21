<?php 
include "config.php";
?>
<!DOCTYPE html>
<html lang="en">
    <head>
        <title>TexMaker</title>
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
              <a class="navbar-brand" href="">TexMaker</a>
            </div>
            <div id="navbar" class="navbar-collapse collapse">
              <ul class="nav navbar-nav">
                <li class="active"><a href="/index.php">Create PDF</a></li>
              </ul>
            </div><!--/.nav-collapse -->
          </div>
        </nav>

        <div class="container">
            <div class="jumbotron">
                <form onsubmit="senddata(); return false;">
                        <h2>TexMaker</h2>
                        <div class="form-group">
                            <label for="content">Latex</label>
                            <textarea type="content" id="content" name="content" class="form-control" placeholder="\section{Hello world}" required="required" rows="15"></textarea>
                        </div>
                        <br>
                        <div class="form-group">
                            <label for="template">Template</label>
                            <select class="form-control" name="template" id="template">
                                <?php
                                foreach($TEMPLATES as $template) {
                                    echo "<option value='$template'>$template</option>";
                                }
                                ?>
                            </select>
                        </div>
                        <br>
                        <button class="btn btn-lg btn-primary btn-block" type="submit">Generate PDF!</button>
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
