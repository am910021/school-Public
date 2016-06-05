$("button[class~='move-up']").on('click', function(e) {
    var value=this.value;
    $('#UP').val(value);
    $('#MOVEForm').submit();
});

$("button[class~='move-down']").on('click', function(e) {
	var value=this.value;
	$('#DOWN').val(value);
	$('#MOVEForm').submit();
});

$("button[class~='remove']").on('click', function(e) {
	var value=this.value.split(",");
	if (!confirm("是否要刪除 "+value[1]+" 選單")){
        return false;
    }
    $('#menuID').val(value[0]);
    $('#menuName').val(value[1]);
    $('#removeForm').submit();
});

$("#resetOrder").on('click', function(e) {
    if (!confirm("是否要重置排序？ 重置後就無法回復")){
        return false;
    }
    $('#resetOrderForm').submit();
});

$("tbody tr:even").addClass('info');