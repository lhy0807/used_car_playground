// Call the dataTables jQuery plugin
$(document).ready(function() {
    let modeltable = $('#dataTable').DataTable({
        dom: 'Bfrtip',
        select: {
            style: 'multi'
        },
        "lengthMenu": [
            [5, 10, 25, -1],
            [5, 10, 25, "All"]
        ],
        buttons: [{
            text: 'Submit',
            action: function() {
                let req = [];
                let selectedModels = modeltable.rows({ selected: true }).data().toArray();
                for (i = 0; i < selectedModels.length; i++) {
                    req.push(selectedModels[i][0]);
                }
                document.getElementsByName('code')[0].value = JSON.stringify(req);
                document.getElementsByName('codeform')[0].submit();
            }
        }]
    });
});