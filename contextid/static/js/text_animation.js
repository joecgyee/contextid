const textElement = document.getElementById('typed-text');
const words = ["Adaptive.", "Secure.", "Simple."];
let wordIndex = 0;
let charIndex = 0;
let isDeleting = false;
let typeSpeed = 150;

function type() {
    const currentWord = words[wordIndex];
    
    if (isDeleting) {
        // Remove characters
        textElement.textContent = currentWord.substring(0, charIndex - 1);
        charIndex--;
        typeSpeed = 75; // Faster when deleting
    } else {
        // Add characters
        textElement.textContent = currentWord.substring(0, charIndex + 1);
        charIndex++;
        typeSpeed = 150;
    }

    // If word is complete
    if (!isDeleting && charIndex === currentWord.length) {
        isDeleting = true;
        typeSpeed = 2000; // Pause at the end of the word
    } else if (isDeleting && charIndex === 0) {
        isDeleting = false;
        wordIndex = (wordIndex + 1) % words.length;
        typeSpeed = 500; // Small pause before starting next word
    }

    setTimeout(type, typeSpeed);
}

// Start the animation when the DOM is loaded
document.addEventListener('DOMContentLoaded', type);