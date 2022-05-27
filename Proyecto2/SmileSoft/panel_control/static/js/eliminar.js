// const btnsEliminacion = document.querySelectorAll(".btnEliminacion");


(function () {

    const btnEliminacion = document.querySelectorAll(".btnEliminacion");

    btnEliminacion.forEach((btn) => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            Swal.fire({
                title: '¿Esta seguro que desea eliminar?',
                text: "La operación no se podrá deshacer",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Aceptar',
                cancelmButtonText: 'Cancelar',
                backdrop: true,
                showLoarderonConfirm: true,
                preConfirm: () => {
                    console.log("Confirmado");
                    Swal.fire({
                        title: 'Eliminado correctamente',
                        icon: 'success',
                        timer: 5000,
                    });
                    location.href = e.target.href;  
                },
                allowOutsideClick: () => false,
                allowEscapeKey: () => false,

            });
        });
    });
})();





// (function () {
//     Swal.fire({
//         title: '¿Estás seguro que quiere eliminar este usuario?',
//         text: "La operación no se podrá deshacer",
//         icon: 'warning',
//         showCancelButton: true,
//         confirmButtonColor: '#3085d6',
//         cancelButtonColor: '#d33',
//         confirmButtonText: 'Aceptar',
//         cancelmButtonText: 'Cancelar',
//     }).then((result) => {
//         if (result.value) {
//             window.location.href = "/sesion/eliminar_usuario/" + usuario,
//                 Swal.fire({
//                     title: 'Eliminado correctamente',
//                     icon: 'success',
//                     timer: 5000,
//                 });
//         } else {
//             swal.fire({
//                 title: "La eliminación fue cancelada",
//                 timer: 2000,
//             });
//         }
//     });
// });

// const btnsEliminacion = document.querySelectorAll(".btnEliminacion");
// (function confirmarEliminacion(usuario) {
//     Swal.fire({
//         title: '¿Estás seguro que quiere eliminar este usuario?',
//         text: "La operación no se podrá deshacer",
//         icon: 'warning',
//         showCancelButton: true,
//         confirmButtonColor: '#3085d6',
//         cancelButtonColor: '#d33',
//         confirmButtonText: 'Aceptar',
//         cancelmButtonText: 'Cancelar',
//     }).then((result) => {
//         if (result.value) {
//             window.location.href = `/sesion/listar_usuario/${usuario}/`;


//         }
//     })
// });
