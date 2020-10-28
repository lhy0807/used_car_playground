// Call the dataTables jQuery plugin
$(document).ready(function() {
    $('#dataTable').DataTable({
        "lengthMenu": [
            [5, 10, 25, -1],
            [5, 10, 25, "All"]
        ]
    });
});