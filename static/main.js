$(document).ready(function() {
    $('table.display').DataTable();

    var change = $('#change').dataTable();
    // Sort immediately with column 2 (at position 1 in the array (base 0). More could be sorted with additional array elements
    change.fnSort( [ [0,'desc'] ] );

    var accum = $('#accum').dataTable();
    // And to sort another column descending (at position 2 in the array (base 0).
    accum.fnSort( [ [2,'desc'] ] );
} );


