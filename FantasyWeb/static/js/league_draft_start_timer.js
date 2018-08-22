$(document).ready(function(){
	var draft_time = document.getElementById("draft_time_value");
	if(draft_time !== null){
		var countDownDate = new Date(draft_time.innerHTML).getTime();

		// Update the count down every 1 second
		var x = setInterval(function() {
			// Get todays date and time
			var now = new Date().getTime();

			// Find the distance between now and the count down date
			var distance = countDownDate - now;

			// Time calculations for days, hours, minutes and seconds
			var days = Math.floor(distance / (1000 * 60 * 60 * 24));
			var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
			var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
			var seconds = Math.floor((distance % (1000 * 60)) / 1000);

			var printed_time = "";
			if(days > 0){
				printed_time += days + " day";
                if(days != 1){
                    printed_time += "s";
                }
                printed_time += " ";
			}
			if(days > 0 || hours > 0){
				printed_time += hours + " hour";
                if(hours != 1){
                    printed_time += "s";
                }
                printed_time += " ";
			}
			if(days > 0 || hours > 0 || minutes > 0){
				printed_time += minutes + " min ";
			}
			printed_time += seconds + " sec";

			// Output the result in an element with id="time_until_draft"
			document.getElementById("time_until_draft").innerHTML = printed_time;

			// If the count down is over, write some text
			if (distance < 0) {
				clearInterval(x);
				document.getElementById("time_until_draft").innerHTML = "Live Now!";
			}
		}, 1000);
	}
});
