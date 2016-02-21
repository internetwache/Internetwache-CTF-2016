<?php
	include "config.php";
	if(isset($_POST['content']) && isset($_POST['template']) && in_array($_POST['template'], $TEMPLATES)) {
		$TEMPLATE = $_POST['template'];
		$CONTENT = $_POST['content'];

		$USERID = md5(time() . ":" . microtime());
		$USERDIR = $COMPILEDIR . $USERID;

		$header = file_get_contents($TEMPLATEDIR . $TEMPLATE . "/header.tex");
		$footer = file_get_contents($TEMPLATEDIR . $TEMPLATE . "/footer.tex");

		$content = $header.$CONTENT.$footer;

		if(preg_match("(input|include)", $CONTENT)) {
			echo 'BLACKLISTED commands used';
		} else {
			file_put_contents($USERDIR . ".tex", $content);

			$CMD = "cd $COMPILEDIR && $PDFLATEX --shell-escape $USERID.tex";
			$output = shell_exec($CMD);

			if(file_exists($USERDIR . ".pdf")) {
				rename($USERDIR . ".pdf", $OUTPUTDIR . $USERID . ".pdf");
				echo "FILE CREATED: $USERID.pdf\n";
				echo "Download: $DLURL$USERID.pdf\n";
			}

			@unlink($USERDIR . ".tex");
			@unlink($USERDIR . ".log");
			@unlink($USERDIR . ".aux");


			echo "\n\nLOG:\n";
			echo $output;
		}
	} else {
		echo 'Error, wrong data';
	}
?>