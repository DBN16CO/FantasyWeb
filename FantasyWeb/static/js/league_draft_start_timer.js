$(document).ready(function(){
    function createTimeRemainingString(distance) {
        var days = Math.floor(distance / (1000 * 60 * 60 * 24));
        var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        var seconds = Math.floor((distance % (1000 * 60)) / 1000);

        var printedTime = "";
        if(days > 0){
            printedTime += days + ((days !== 1)? " days ": " day ");
        }
        if(days + hours > 0){
            printedTime += hours + ((hours !== 1)? " hours ": " hour ");
        }
        if(days + hours + minutes > 0){
            printedTime += minutes + " min ";
        }
        printedTime += seconds + " sec";

        return printedTime;
    }

	var draftTime = document.getElementById("draft_time_value");
	if(draftTime !== null){
		var countDownDate = new Date(draftTime.textContent).getTime();

		// Update the count down every 1 second
		var x = setInterval(function() {
			// Get todays date and time
			var now = new Date().getTime();

			// Find the distance between now and the count down date
			var distance = countDownDate - now;

			// Time calculations for days, hours, minutes and seconds
		    var printedTime = createTimeRemainingString(distance);

			// Output the result in an element with id="time_until_draft"
			document.getElementById("time_until_draft").textContent = printedTime;

			// If the count down is over, write some text
			if (distance < 0) {
				clearInterval(x);
				document.getElementById("time_until_draft").textContent = "Live Now!";
			}
		}, 1000);
	}
});
