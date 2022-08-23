function toggle_form() {
  // Get the checkbox
  var checkBox = document.getElementById("Web_source_toggle");
  // Get the output text
  var text = document.getElementById("id_recipe_source_link");

  // If the checkbox is checked, display the output text
  if (checkBox.checked == true){
    text.style.display = "block";
  } else {
    text.style.display = "none";
  }
}