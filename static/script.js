const body = document.querySelector("body"), 
btn = document.querySelector(".link-name");

let getMode = localStorage.getItem("mode");
if(getMode && getMode ==="dark"){
    body.classList.toggle("dark");
}

btn.addEventListener("click", () => {
    body.classList.toggle("dark");
    console.log(btn.innerHTML)
    if(btn.innerHTML == "Koyu Mod"){
        btn.innerHTML = "Açık Mod"
    }
    else{
        btn.innerHTML= "Koyu Mod"
    }
    if(body.classList.contains("dark")){
        localStorage.setItem("mode", "dark");
    }else{
        localStorage.setItem("mode", "light");
    }
})

