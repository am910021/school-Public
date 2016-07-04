$(document).ready(function() {
	$('tbody>tr:even').addClass("info");
    $('#tr-search').on('keyup', function() {
        var keyword = $('#tr-search').val();
        if (keyword !== '') {
            $('tbody>tr').css("display", "none");
            $('tbody>tr').find(":contains('" + keyword + "')").parent().attr("style", "")
        } else {
            $('tbody>tr').attr("style", "")
        }
    });
    
    $('button[class~="redirect"]').on('click', function() {
    	//alert(this.value)
    	document.location = this.value;
    });
    
    $('button[class~="remove"]').on('click', function() {
    	var value=this.value.split(",");
        if (!confirm("是否要刪除 "+value[1]+" 帳號？")){
            return false;
        }
        $('#accountID').val(value[0]);
        $('#accountName').val(value[1]);
        $('#removeForm').submit();
    })   
});