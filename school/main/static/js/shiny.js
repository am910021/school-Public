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
        document.getElementById('shinyapp' + i).style.display = 'none';
      }
      document.getElementById('shinyapp' + id).style.display = 'block';
    });

    function openInNewTab(url) {
      var win = window.open(url, '_blank');
      win.focus();
    }

  });