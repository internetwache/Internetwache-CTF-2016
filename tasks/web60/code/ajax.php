<?php
include "flag.php";
if(isset($_POST['search']) && isset($_POST['replace']) && isset($_POST['content'])) {

	if(preg_match("(system|file|open|exec|pass|eval|call_user_func)",$_POST['replace'])) {
		die('Blacklisted keywords!');
	}

	$new = preg_replace($_POST['search'], $_POST['replace'], $_POST['content']);
	echo $new;
}
?>