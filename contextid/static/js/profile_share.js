/**
 * Captures a card element and downloads it as a PNG image.
 * @param {HTMLElement} btn - The button element that triggered the function.
 */

function downloadCard(btn) {
    const card = document.getElementById('profileCard');
    
    // Retrieve the dynamic filename from the data attribute on the button
    const filename = btn.getAttribute('data-filename') || 'profile-card';
    
    // Ensure html2canvas is loaded
    if (typeof html2canvas === 'undefined') {
        console.error('html2canvas library is not loaded.');
        return;
    }

    // We use a small timeout to ensure the UI feels responsive
    html2canvas(card, {
        useCORS: true, // Crucial for loading images from different domains/media settings
        backgroundColor: "#ffffff", // Ensures the background isn't transparent
        scale: 2 // Increases quality/resolution of the image

    }).then(canvas => {
        const link = document.createElement('a');
        link.download = filename + '.png';
        link.href = canvas.toDataURL("image/png");
        link.click();
    });
}