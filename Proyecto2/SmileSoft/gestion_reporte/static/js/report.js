var date_range = null;
var date_now = new moment().format('YYYY-MM-DD');

function generate_report() {
    var parameters = {
        'action': 'search_report',
        'start_date': date_now,
        'end_date': date_now,
    };

    if (date_range !== null) {
        parameters['start_date']= date_range.startDate.format('YYYY-MM-DD');
        parameters['end_date'] = date_range.endDate.format('YYYY-MM-DD');
    }

   $('#data').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: parameters,
            dataSrc: ""
        },
//         columns: [
//             { "data": "id_cita" },
//             { "data": "tratamiento_solicitado" },
           
//             { "data": "fecha" },
            
//         ],
//         columnDefs: [
//             {
//                 targets: [-1, -2, -3],
//                 class: 'text-center',
//                 orderable: false,
//                 render: function (data, type, row) {
//                     return '%' + parseFloat(data).toFixed(2);
//                 }
//             },
//         ],
        initComplete: function (settings, json) {

        }
    });
}


$(function () {
    $('input[name="date_range"]').daterangepicker({
         locale : {
            format: 'YYYY-MM-DD',
            applyLabel: '<i class="fas fa-chart-pie"></i> Apli',
            cancelLabel: '<i class="fas fa-times"></i> Cancelar',
        }
    });
    // }).on('apply.daterangepicker', function (ev, picker) {
    //     date_range = picker;
    //     generate_report();
    //     console.log(picker.setStartDate.format('YYYY-MM-DD')+'-'+ picker.endDate.format('YYYY-MM-DD'));
        
    // }).on('cancel.daterangepicker', function (ev, picker) {
    //     $(this).data('daterangepicker').setStartDate(date_now);
    //     $(this).data('daterangepicker').setEndDate(date_now);
    //     date_range = picker;
    //     generate_report();
    // });

    generate_report();
});