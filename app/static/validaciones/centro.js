function eliminarCentro() {
  if (
    confirm(
      "¿Esta seguro que desea eliminar el Centro? Se CANCELARAN los turnos para este centro"
    )
  ) {
    return true;
  } else {
    return false;
  }
}
function aceptarCentro() {
  if (confirm("¿Esta seguro que desea aceptar el centro?")) {
    return true;
  } else {
    return false;
  }
}

function rechazarCentro() {
  if (confirm("¿Esta seguro que desea rechazar el centro?")) {
    return true;
  } else {
    return false;
  }
}

function publicarCentro() {
  if (confirm("¿Esta seguro que desea publicar el centro?")) {
    return true;
  } else {
    return false;
  }
}

function despublicarCentro() {
  if (confirm("¿Esta seguro que desea despublicar el centro?")) {
    return true;
  } else {
    return false;
  }
}

function validarCentro() {
  if (document.getElementById("nombre").value == "") {
    alert("El campo nombre no puede estar vacío");
    return false;
  }
  if (document.getElementById("direccion").value == "") {
    alert("El campo dirección no puede estar vacío");
    return false;
  }
  if (document.getElementById("telefono").value == "") {
    alert("El campo telefono no puede estar vacío");
    return false;
  }

  for (i = 0; i < document.getElementById("telefono").value.length; i++) {
    if (
      !(
        numeros.indexOf(
          document.getElementById("telefono").value.charAt(i),
          0
        ) != -1
      )
    ) {
      alert("El campo telefono solo puede contener números");
      return false;
    }
  }

  if (document.getElementById("apertura").value == "") {
    alert("El campo horario de apertura no puede estar vacío");
    return false;
  }

  if (document.getElementById("cierre").value == "") {
    alert("El campo horario de cierre no puede estar vacío");
    return false;
  }
  if (
    document.getElementById("apertura").value >=
    document.getElementById("cierre").value
  ) {
    alert("El horario de apertura debe ser menor que el horario de cierre");
    return false;
  }
  if (document.getElementById("tipo_centro").value == "0") {
    alert("No ha seleccionado un tipo de centro válido");
    return false;
  }
}
