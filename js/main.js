// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Navbar scroll behavior
window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('navbar-scrolled');
    } else {
        navbar.classList.remove('navbar-scrolled');
    }
});

// Initialize tooltips
var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl);
});

// Add animation on scroll
function revealOnScroll() {
    var reveals = document.querySelectorAll(".reveal");

    reveals.forEach((reveal) => {
        var windowHeight = window.innerHeight;
        var elementTop = reveal.getBoundingClientRect().top;
        var elementVisible = 150;

        if (elementTop < windowHeight - elementVisible) {
            reveal.classList.add("active");
        }
    });
}

window.addEventListener("scroll", revealOnScroll);

// Handle mobile menu
const mobileMenu = document.querySelector('.navbar-toggler');
const navLinks = document.querySelectorAll('.nav-link');

navLinks.forEach(link => {
    link.addEventListener('click', () => {
        if (window.innerWidth < 992) {
            document.querySelector('.navbar-collapse').classList.remove('show');
        }
    });
});

// Function to save event data to the server
async function saveEventData(formData) {
    try {
        const response = await fetch('/api/customize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();
        console.log('Server response:', result);

        if (result.status === 'success') {
            // Store event data in localStorage
            localStorage.setItem('customEvent', JSON.stringify(formData));
            // Redirect to checkout page
            window.location.href = 'checkout.html?type=event';
            return true;
        } else {
            alert('There was an error submitting your request. Please try again.');
            return false;
        }
    } catch (error) {
        console.error('Error:', error);
        alert('There was an error submitting your request. Please try again.');
        return false;
    }
}