$(document).ready(function(){
	var dtSettings = {
		"searching": true,
		"paging": true,
		"info": false,
		"oLanguage": {
			"sEmptyTable": "There are no remaining active free agents"
		}
	};
	$("#free-agents-table").DataTable(dtSettings);
});
