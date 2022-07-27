
//slide for news
var slideIndex = 1;


// Next/previous controls
function plusSlides(n) {
  showSlides(slideIndex += n);
}

// Thumbnail image controls
function currentSlide(n) {
  showSlides(slideIndex = n);
}

function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("mySlides");

  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
  }

  slides[slideIndex-1].style.display = "block";

} 



//slide for stocks
var slidesIndex = 1;


// Next/previous controls
function plusSlide(n) {
  showSlide(slidesIndex += n);
}

// Thumbnail image controls
function currentSlides(n) {
  showSlide(slidesIndex = n);
}

function showSlide(n) {
  var i;
  var slides = document.getElementsByClassName("stockSlides");

  if (n > slides.length) {slidesIndex = 1}
  if (n < 1) {slidesIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
  }

  slides[slidesIndex-1].style.display = "block";

} 


//unused slide for portfolio
var slidesIndex1 = 1;


// Next/previous controls
function plusSlide1(n) {
  showSlide1(slidesIndex += n);
}

// Thumbnail image controls
function currentSlides1(n) {
  showSlide1(slidesIndex = n);
}

function showSlide1(n) {
  var i;
  var slides = document.getElementsByClassName("stockSlidess");

  if (n > slides.length) {slidesIndex = 1}
  if (n < 1) {slidesIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
  }

  slides[slidesIndex-1].style.display = "block";

} 

function openNav() {
  document.getElementById("mySidepanel").style.display = "inline";
  document.getElementById("tog").style.display = "none";
}

/* Set the width of the sidebar to 0 (hide it) */
function closeNav() {
  document.getElementById("mySidepanel").style.display = "none";
  document.getElementById("tog").style.display = "inline";
} 