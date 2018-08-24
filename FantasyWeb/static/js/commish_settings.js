$(document).ready(function(){
	function copyStringToClipboard (str) {
		// Create new element
		var el = document.createElement("textarea");
		// Set value (string to be copied)
		el.value = str;
		// Set non-editable to avoid focus and move outside of view
		el.setAttribute("readonly", "");
		el.style = {position: "absolute", left: "-9999px"};
		document.body.appendChild(el);
		// Select text inside element
		el.select();
		// Copy text to clipboard
		document.execCommand("copy");
		// Remove temporary element
		document.body.removeChild(el);
	}
	$("#copy-btn").on("click", function(){
		copyStringToClipboard($("#invite-link").text());
	});


    $('#datetimepicker1').datetimepicker();
   

    $("#draft-time-form").submit(function(){
	    // Let's find the input to check
	    var input = $(this).find("input[name=datetime]");
	    if (input.val()) {
	        var picker = $('#datetimepicker1').data('datetimepicker');
	        console.log(picker);
	//      alert(input.val());
	//      alert(picker.getLocalDate().toISOString());
	        input.val(picker.viewDate().toISOString());
	        console.log(input.val());
	        }
	    });
});
