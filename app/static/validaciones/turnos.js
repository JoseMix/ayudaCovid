function confirmationTurno() {
    if(confirm("Esta seguro que desea cancelar el turno?")) {
        return true;
    } else {
        return false;
    }
}

function validarDatosTurno(){
    if ( (document.getElementById("dia").value=="" ) ){ 
        alert("El campo fecha no puede estar vacío");
        return false;
    }
    if ((document.getElementById("email").value=="")){
        alert("El campo mail no puede estar vacío");
        return false;
    }
    if ( (document.getElementById("bloque").value=="" ) ){ 
        alert("El campo franja horaria no  puede estar vacío");
        return false;
    }    
}
