	$(document).ready(function() {
	    $('#multiselect').multiselect({
	        right: '#added',
	        undo: '#undo',
	        rightAll: '#rightAll',
	        rightSelected: '#rightSelected',
	        leftSelected: '#leftSelected',
	        leftAll: '#leftAll',
	        redo: '#redo',
	        search: {
	            left: '<input type="text" name="q" class="form-control" placeholder="搜尋..." />'
	        },
	    });

	    $('#multiselect2').multiselect({
	        right: '#added2',
	        undo: '#undo2',
	        rightAll: '#rightAll2',
	        rightSelected: '#rightSelected2',
	        leftSelected: '#leftSelected2',
	        leftAll: '#leftAll2',
	        redo: '#redo2',
	        search: {
	            left: '<input type="text" name="q" class="form-control" placeholder="搜尋..." />'
	        },
	    });


	    $('#form1').on('submit', function() {
	        var $name = $('#id_name');
	        var $select = $('#added');
	        var $select2 = $('#added2');
	        var pass = true;
	        if ($select2.children().length == 0) {
	            $select2.parent().addClass('has-error has-feedback');
	            $select2.focus();
	            pass = false;
	        }
	        if ($select.children().length == 0) {
	            $select.parent().addClass('has-error has-feedback');
	            $select.focus();
	            pass = false;
	        }
	        if ($name.val().length == 0) {
	            $name.parent().attr('class', 'form-group has-error has-feedback');
	            $name.parent().append('<span id="error-icon" class="glyphicon glyphicon-remove form-control-feedback" aria-hidden="true"></span>');
	            $name.focus();
	            pass = false;
	        }

	        if (!pass) {
	            return false;
	        }
	        this.action = postUrl;
	        this.submit();
	    });


	    $('#id_name').on('change', function() {
	        var $name = $(this);
	        if (this.value.length > 0) {
	            $name.parent().attr('class', 'form-group has-success has-feedback');
	            $name.parent().append('<span id="success-icon" class="glyphicon glyphicon-ok form-control-feedback" aria-hidden="true"></span>');
	            $('#error-icon').remove();
	        } else {
	            $name.parent().attr('class', 'form-group has-error has-feedback');
	            $name.parent().append('<span id="error-icon" class="glyphicon glyphicon-remove form-control-feedback" aria-hidden="true"></span>');
	            $('#success-icon').remove();
	        }
	    });

	    $('select[class~="right-select"]').on('DOMSubtreeModified', function() {
	        var $this = $(this)
	        if ($this.children().length == 0) {
	            $this.parent().addClass('has-error has-feedback');
	        } else {
	            $this.parent().removeClass('has-error has-feedback');
	        }
	    });
	    
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
	        if (!confirm("是否要刪除 "+value[1]+" 權限？")){
	            return false;
	        }
	        $('#groupID').val(value[0]);
	        $('#groupName').val(value[1]);
	        $('#removeForm').submit();
	    });
	});