function senddata() {
	var content = $("#content").val();
	var template = $("#template").val();

	if(content == "") {
		$("#output").text("No input given!");
	}
	$.ajax({
		url: "ajax.php",
		data: {
			'content':content,
			'template':template
		},
		method: 'post'
	}).success(function(data) {
		$("#output").text(data)
	}).fail(function(data) {
		$("#output").text("OOps, something went wrong...\n"+data)
	})
	return false;
}