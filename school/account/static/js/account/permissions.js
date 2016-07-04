$(document).ready(function() {
    $('#tr-search').on('keyup', function() {
        var keyword = $('#tr-search').val();
        if (keyword !== '') {
            $('tbody>tr').css("display", "none");
            $('tbody>tr').find(":contains('" + keyword + "')").parent().attr("style", "")
        } else {
            $('tbody>tr').attr("style", "")
        }
    });
    $('tbody>tr:even').addClass('info');
    
    $('button[class~="redirect"]').on('click', function(){
    	//alert(this.value)
    	document.location = this.value;
    })
});