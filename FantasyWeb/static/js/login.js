function loadAsRegister() {
    $("#login-form").hide();
    $("#register-form").show();
    $("#login-form-link").removeClass('active');
    $("#register-form-link").addClass('active');
}

$(document).ready(function() {
    $("#login-form-link").click(function(e) {
        $("#login-error").fadeOut(100);
        $("#register-error").fadeOut(100);
		$("#login-form").delay(100).fadeIn(100);
 		$("#register-form").fadeOut(100);
		$("#register-form-link").removeClass('active');
		$(this).addClass('active');
		e.preventDefault();
	});
	$("#register-form-link").click(function(e) {
        $("#login-error").fadeOut(100);
        $("#register-error").fadeOut(100);
		$("#register-form").delay(100).fadeIn(100);
 		$("#login-form").fadeOut(100);
		$("#login-form-link").removeClass('active');
		$(this).addClass('active');
		e.preventDefault();
	});
    $('input:text').focus(function() {
        $("#login-error").fadeOut(100);
        $("#register-error").fadeOut(100);
    });
});
