window.addEventListener("load", () => {
  /* --------------------------------
  Page loader 
  -----------------------------------*/ 
  document.querySelector(".js-page-loader").classList.add("fade-out");
  setTimeout(() => {
    document.querySelector(".js-page-loader").style.display = "none";
  }, 600);
});

