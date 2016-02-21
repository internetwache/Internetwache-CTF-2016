<?php

for($i=0; $i<1000000000; $i++) {
	$str = $i;
	$hash = md5(md5($str) . "SALT");
	if(preg_match("/^0e[0-9]+$/", $hash)) {
		echo $str." : ".$hash."\n";
	}
	//62778807 : 0e774261293712168181959463563504
}
