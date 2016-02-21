$("#flag-submission").click(function() {
	submit();
});

$(document).keypress(function( event ) {
	if(event.which == 13) {
		event.preventDefault();
		submit();
	}
});
function submit() {
    var cat = $(".task-box").data("category");
    var score = $(".task-box").data("score");
    var flag = $("#flag-input").val();
    var csrf = $("#_csrf_token").val();

    $.ajax({
        url: "/task/submit",
        method: "POST",
        data: {"category": cat, "score":score, "flag": btoa(flag), "_csrf_token": csrf}
    }).done(function(data) {
        $("#_csrf_token").val(data['csrf']);
        $("#flag-output").fadeIn(900);
	if (data["success"]) {
            $("#flag-output").html($(".lang").data("success"));
            $("#flag-submission").removeClass("btn-primary");
            $("#flag-submission").addClass("btn-success");
            $("#flag-submission").attr('disabled','disabled');
        } else {
            $("#flag-output").html($(".lang").data("failure"));
        }
	$("#flag-output").fadeOut(1000);
    });
}
