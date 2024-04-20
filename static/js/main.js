window.addEventListener("load", () => {
  /* --------------------------------
  Page loader 
  -----------------------------------*/ 
  document.querySelector(".js-page-loader").classList.add("fade-out");
  setTimeout(() => {
    document.querySelector(".js-page-loader").style.display = "none";
  }, 600);
});

/* ----------------------------- 
 header menu 
 -------------------------------*/
function headerMenu(){
  const menu = document.querySelector(".js-header-menu"),
  backdrop = document.querySelector(".js-header-backdrop"),
  menuCollapseBreakpoint = 991;

  function toggleMenu(){
    menu.classList.toggle("open");
    backdrop.classList.toggle("active");
    document.body.classList.toggle("overflow-hidden");
  }

  document.querySelectorAll(".js-header-menu-toggler").forEach((item) => {
    item.addEventListener("click", toggleMenu);
  });

}