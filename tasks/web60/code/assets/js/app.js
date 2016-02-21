function senddata() {
	var search = $("#search").val();
	var replace = $("#replace").val();
	var content = $("#content").val();

	if(search == "" || replace == "" || content == "") {
		$("#output").text("No input given!");
	}
	$.ajax({
		url: "ajax.php",
		data: {
			'search':search,
			'replace':replace,
			'content':content
		},
		method: 'post'
	}).success(function(data) {
		$("#output").text(data)
	}).fail(function(data) {
		$("#output").text("OOps, something went wrong...\n"+data)
	})
	return false;
}