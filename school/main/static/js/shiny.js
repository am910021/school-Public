  $(document).ready(function() {
    var os = navigator.platform.toLowerCase();
    if (os == "iphone" || os == "android")
      $('#app-position').remove();

    $('button.fork').on('click', function() {
      var id = $(this).val();
      if (os == "iphone" || os == "android"){
    	  openInNewTab("/shiny/apps/"+appNames[id-1]+"/")
    	  return;
      }

      for (i = 1; i <= totalApps; i++) {
	
        document.getElementById('shinyapp' + i).style.visibility = 'hidden';
	document.getElementById('shinyapp' + i).style.height = '0px';
      }
	document.getElementById('shinyapp' + id).removeAttribute("style")
    });

    function openInNewTab(url) {
      var win = window.open(url, '_blank');
      win.focus();
    }

  });