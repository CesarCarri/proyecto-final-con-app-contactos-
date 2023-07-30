// document.addEventListener("DOMContentLoaded", function () {
//     const deleteButtons = document.querySelectorAll(".btn-delete");
  
//     deleteButtons.forEach((button) => {
//       button.addEventListener("click", function (event) {
//         event.preventDefault();
//         const articleTitle = this.getAttribute("data-article-title");
//         const confirmDelete = confirm(`¿Estás seguro de que deseas eliminar el artículo "${articleTitle}"?`);
  
//         if (confirmDelete) {
//           // Si el usuario confirma la eliminación, enviar el formulario de eliminación
//           const form = this.parentElement;
//           form.submit();
//         }
//       });
//     });
//   });
  