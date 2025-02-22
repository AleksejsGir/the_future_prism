document.addEventListener("DOMContentLoaded", function() {
    const searchBtn = document.getElementById("mobile-search-btn");
    const searchBox = document.getElementById("mobile-search-box");

    if (searchBtn && searchBox) {
        searchBtn.addEventListener("click", function() {
            if (searchBox.classList.contains("active")) {
                searchBox.classList.add("hidden");
                setTimeout(() => {
                    searchBox.classList.remove("active", "hidden");
                    searchBox.style.display = "none";
                }, 300);
            } else {
                searchBox.style.display = "block";
                searchBox.classList.add("active");
            }
        });
    }
});
