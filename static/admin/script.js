
const openBtn = document.getElementById("openModal");
const closeBtn = document.getElementById("closeModal");
const modal = document.getElementById("modal");


openBtn.addEventListener("click", () => {
    modal.classList.add("open");
});

closeBtn.addEventListener("click", () => {
    modal.classList.remove("open");
});


const openBtnService = document.getElementById("openModalService");
const closeBtnService = document.getElementById("closeModalService");
const modalService = document.getElementById("modalService");


openBtnService.addEventListener("click", () => {
    modalService.classList.add("open");
});

closeBtnService.addEventListener("click", () => {
    modalService.classList.remove("open");
});





function updatePlaceholder() {
    var selectElement = document.getElementById("mySelect");
    var inputElement = document.getElementById("unitMeasure");
    var selectedValue = selectElement.value;

    if (selectedValue === "option1") {
      inputElement.value = "Kilogrammes";
    } else if (selectedValue === "option2") {
      inputElement.value = "Paquets";
    } else if (selectedValue === "option3") {
      inputElement.value = "Sacs";
    }
  }

function updatePlaceholderService() {
    var selectElementService = document.getElementById("mySelectService");
    var inputElementService = document.getElementById("unitMeasureService");
    var selectedValueService = selectElementService.value;

    if (selectedValueService === "option1Service") {
      inputElement.value = "Kilogrammes";
    } else if (selectedValueService === "option2Service") {
      inputElement.value = "Paquets";
    } else if (selectedValueService === "option3Service") {
      inputElement.value = "Sacs";
    }
  }



















const allSideMenu = document.querySelectorAll('#sidebar .side-menu.top li a');

allSideMenu.forEach(item=> {
   const li = item.parentElement;

   item.addEventListener('click', function () {
      allSideMenu.forEach(i=> {
         i.parentElement.classList.remove('active');
      })
      li.classList.add('active');
   })
});




// TOGGLE SIDEBAR
const menuBar = document.querySelector('#content nav .bx.bx-menu');
const sidebar = document.getElementById('sidebar');

menuBar.addEventListener('click', function () {
   sidebar.classList.toggle('hide');
})







const searchButton = document.querySelector('#content nav form .form-input button');
const searchButtonIcon = document.querySelector('#content nav form .form-input button .bx');
const searchForm = document.querySelector('#content nav form');

searchButton.addEventListener('click', function (e) {
   if(window.innerWidth < 576) {
      e.preventDefault();
      searchForm.classList.toggle('show');
      if(searchForm.classList.contains('show')) {
         searchButtonIcon.classList.replace('bx-search', 'bx-x');
      } else {
         searchButtonIcon.classList.replace('bx-x', 'bx-search');
      }
   }
})





if(window.innerWidth < 768) {
   sidebar.classList.add('hide');
} else if(window.innerWidth > 576) {
   searchButtonIcon.classList.replace('bx-x', 'bx-search');
   searchForm.classList.remove('show');
}


window.addEventListener('resize', function () {
   if(this.innerWidth > 576) {
      searchButtonIcon.classList.replace('bx-x', 'bx-search');
      searchForm.classList.remove('show');
   }
})

const switchMode = document.getElementById('switch-mode');
switchMode.addEventListener('change', function () {
   if(this.checked) {
      document.body.classList.add('dark');
   } else {
      document.body.classList.remove('dark');
   }
})
