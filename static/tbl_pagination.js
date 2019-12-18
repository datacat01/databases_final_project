$(document).ready( function () {
    $('#pagin_tbl').DataTable();
} );

// $(document).ready(function () {
//     $('#sales_tbl').DataTable({
//       bProcessing: true,
//       bServerSide: true,
//       sPaginationType: "full_numbers",
//       lengthMenu: [[10, 25, 50, 100], [10, 25, 50, 100]],
//       bjQueryUI: true,
//       sAjaxSource: '<API_ENDPOINT>',
//       columns: [
//         {"data": "id"},
//         {"data": "Order id"},
//         {"data": "Payment time"},
//         {"data": "Price"}
//       ]
//     });
//   });