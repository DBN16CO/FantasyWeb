$(document).ready(function(){
	var qbSettings = {
		"searching": false,
		"paging": false,
		"info": false,
		"oLanguage": {
			"sEmptyTable": "You have no Quarterbacks"
		}
	};
	$("#qb-table").DataTable(qbSettings);

	var rbSettings = {
		"searching": false,
		"paging": false,
		"info": false,
		"oLanguage": {
			"sEmptyTable": "You have no Runningbacks"
		}
	};
	$("#rb-table").DataTable(rbSettings);

	var wrSettings = {
		"searching": false,
		"paging": false,
		"info": false,
		"oLanguage": {
			"sEmptyTable": "You have no Wide Receivers"
		}
	};
	$("#wr-table").DataTable(wrSettings);

	var teSettings = {
		"searching": false,
		"paging": false,
		"info": false,
		"oLanguage": {
			"sEmptyTable": "You have no Tight Ends"
		}
	};
	$("#te-table").DataTable(teSettings);

	var kSettings = {
		"searching": false,
		"paging": false,
		"info": false,
		"oLanguage": {
			"sEmptyTable": "You have no Kickers"
		}
	};
	$("#k-table").DataTable(kSettings);

	var defSettings = {
		"searching": false,
		"paging": false,
		"info": false,
		"oLanguage": {
			"sEmptyTable": "You have no Defenses"
		}
	};
	$("#def-table").DataTable(defSettings);

	var dbSettings = {
		"searching": false,
		"paging": false,
		"info": false,
		"oLanguage": {
			"sEmptyTable": "You have no Defensive Backs"
		}
	};
	$("#db-table").DataTable(dbSettings);

	var lbSettings = {
		"searching": false,
		"paging": false,
		"info": false,
		"oLanguage": {
			"sEmptyTable": "You have no Linebackers"
		}
	};
	$("#lb-table").DataTable(lbSettings);

	var dlSettings = {
		"searching": false,
		"paging": false,
		"info": false,
		"oLanguage": {
			"sEmptyTable": "You have no Defensive Lineman"
		}
	};
	$("#dl-table").DataTable(dlSettings);
});
