const slides = document.getElementsByClassName("slides");
const changeBtn = document.getElementById("change-btn");

let sectionIndex = 0;
const maxslides = slides.length;
console.log("Total slides: ", maxslides);
for (let i = 1; i < slides.length; i++) {
    slides[i].style.display = "none";
}

changeBtn.addEventListener("click", () => {
    slides[sectionIndex].style.display = 'none';
    for (let i = 1; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    sectionIndex++;
    slides[sectionIndex].style.display = "block";
    console.log("current section: ", sectionIndex);
    if (sectionIndex == maxslides - 1) sectionIndex = 0;
})