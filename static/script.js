document.addEventListener("DOMContentLoaded", () => {
  const toggleButton = document.getElementById("theme-toggle");
  const currentTheme = localStorage.getItem("theme") || "light";

  if (currentTheme === "dark") {
    document.documentElement.setAttribute("data-theme", "dark");
    toggleButton.textContent = "🌕"; // Change to sun icon for dark mode
  } else {
    document.documentElement.setAttribute("data-theme", "light");
    toggleButton.textContent = "🌙"; // Change to moon icon for light mode
  }

  toggleButton.addEventListener("click", () => {
    const theme = document.documentElement.getAttribute("data-theme");
    if (theme === "dark") {
      document.documentElement.setAttribute("data-theme", "light");
      localStorage.setItem("theme", "light");
      toggleButton.textContent = "🌙"; // Change to moon icon for light mode
    } else {
      document.documentElement.setAttribute("data-theme", "dark");
      localStorage.setItem("theme", "dark");
      toggleButton.textContent = "🌕"; // Change to sun icon for dark mode
    }
  });
});
