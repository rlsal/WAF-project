$(document).ready(function() {
	$('#alertsTable').DataTable({
		ajax: 'http://localhost:5000/alerts',
		order: [[ 0, "desc" ]]
	});
} );