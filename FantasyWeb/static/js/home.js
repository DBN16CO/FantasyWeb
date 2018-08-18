$(document).ready(function(){
	var dtSettings = {
		"searching": false,
		"paging": false,
		"info": false,
		"oLanguage": {
        	"sEmptyTable": "You are not in any Leagues"
    	}
	}
	$('#test-table').DataTable(dtSettings);
});