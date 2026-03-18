// Navigation Interactions
const navLinks = document.querySelectorAll('nav a');

navLinks.forEach(link => {
    link.addEventListener('click', function() {
        navLinks.forEach(l => l.classList.remove('active'));
        this.classList.add('active');
    });
});

// Smooth Scrolling
const scrollLinks = document.querySelectorAll('a[href^="#"]');

scrollLinks.forEach(link => {
    link.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        target.scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// Dynamic Content Loading
async function loadAssets() {
    const response = await fetch('/api/assets');
    const assets = await response.json();
    console.log(assets);
    // Populate your UI with asset data
}

loadAssets();

// Form Validation
const forms = document.querySelectorAll('form');

forms.forEach(form => {
    form.addEventListener('submit', function(event) {
        const inputs = form.querySelectorAll('input');
        let valid = true;
        inputs.forEach(input => {
            if (!input.value) {
                valid = false;
                input.classList.add('error');
            } else {
                input.classList.remove('error');
            }
        });
        if (!valid) {
            event.preventDefault();
            alert('Please fill in all fields');
        }
    });
});
