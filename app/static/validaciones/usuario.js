function validarUser() {
  if (document.getElementById("username").value == "") {
    alert("El campo username no puede estar vacío");
    return false;
  }
  if (document.getElementById("email").value == "") {
    alert("El campo email no puede estar vacío");
    return false;
  }
  if (document.getElementById("password").value == "") {
    alert("El campo password no puede estar vacío");
    return false;
  }
  if (document.getElementById("first_name").value == "") {
    alert("El campo nombre no puede estar vacío");
    return false;
  }
  if (document.getElementById("last_name").value == "") {
    alert("El campo apellido no puede estar vacío");
    return false;
  }
}
