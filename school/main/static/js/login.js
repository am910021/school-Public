document.domain = document.location.hostname;

var license = document.getElementById("license");
if(license){
license.style="display:none";
var parent_license = parent.document.getElementById("license");
if (parent_license!=""){
        license.value = parent_license.value;
};}
