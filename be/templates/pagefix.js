// split_table inserts page breaks in the table retaining readability of the table across the pages
// this is mainly work around for the chrome problem
// since we generate invoice pdfs using wkhtml this is needed, had we using pisa (xhtml2pdf) or some other pdf generator \ 
// we won't need this hackery. But wkhtml supports css3, html much better than others
// Note that correct top calculation depends on box-sizing:border-box

var step = 1000;
var next_break = 0;

function split_table(idx, the_table) {
    next_break += step;
    // idx is unused, it is there mainly for each() compatibility
    var the_table = $(the_table);
    var tbody = the_table.children('tbody');
    var rows = tbody.children('tr');
    var removed = [];
    for (var i=0; i < rows.length; i++) {
        var row_dom = rows[i];
        var row = $(row_dom);
        var top = row.offset().top;
        if (top > next_break) {
            row.remove();
            removed.push(row);
        };
    };
    if (removed.length) {
        var page_break = $('<div class="page-break"></div>')
        page_break.insertAfter(the_table);
        var new_table = $(the_table.clone());
        new_table.children('tbody').empty();
        new_table.insertAfter(page_break);
        for (var i=0; i < removed.length; i++) {
            new_table.append(removed[i]);
        };
        split_table(0, new_table.children('tbody')[0]);
    };
};

$('table.pagefix').each(split_table);
