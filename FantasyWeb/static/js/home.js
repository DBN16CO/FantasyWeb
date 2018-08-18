$(document).ready(function(){
	var dtSettings = {
		"searching": false,
		"paging": false,
		"info": false,
		"oLanguage": {
			"sEmptyTable": "You are not in any Leagues"
		}
	};
	$("#leagues-table").DataTable(dtSettings);
});