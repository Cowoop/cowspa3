var pagebreak_after = 3600;
var step = 5000;
var pb_table = $('table.pagefix');
var pb_header = $('table.pagefix thead');

function find_top(obj) {
    var top = !!obj.offsetTop ? obj.offsetTop : 0;
    while(obj = obj.offsetParent) {
        top += !!obj.offsetTop ? obj.offsetTop : 0;
    };
    return top;
};

function split_table(the_table, pb_tbody) {
    var pb_tbody = the_table.children('tbody');
    var rows = pb_tbody.children('tr');
    var removed = [];
    for (var i=0; i < rows.length; i++) {
        var row_dom = rows[i];
        var row = $(row_dom);
        var top = row.offset().top;
        var top = row_dom.offsetTop;
        var top = find_top(row_dom);
        if (top > pagebreak_after) {
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
        pagebreak_after = pagebreak_after + step;
        split_table(new_table, new_table.children('tbody'));
    };
};

split_table(pb_table, $('table.pagefix tbody'));
