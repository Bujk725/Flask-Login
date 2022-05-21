const body = document.querySelector("body"), 
btn = document.querySelector(".link-name");

btn.addEventListener("click", () => {
    body.classList.toggle("dark");
})

