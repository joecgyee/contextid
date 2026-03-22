document.addEventListener('DOMContentLoaded', function() {
    const attributeContainer = document.querySelector('#attribute-rows');
    const addButton = document.querySelector('#add-attribute');
    const totalForms = document.querySelector('#id_attributes-TOTAL_FORMS');

    // --- 1. Add New Row Logic (Django Formsets) ---
    if (addButton && attributeContainer && totalForms) {
        addButton.addEventListener('click', function() {
            const currentCount = parseInt(totalForms.value);
            const template = document.querySelector('#empty-form').innerHTML;
            
            const newRowHtml = template.replace(/__prefix__/g, currentCount);
            
            const newRow = document.createElement('div');
            newRow.innerHTML = newRowHtml;
            attributeContainer.appendChild(newRow);

            totalForms.value = currentCount + 1;
            setupVisibility(newRow);
        });
    }

    // --- 2. Conditional Visibility Logic ---
    function setupVisibility(row) {
        const typeSelect = row.querySelector('select[name$="-value_type"]');
        if (!typeSelect) return;

        const fields = {
            'value_string': row.querySelector('div[id$="-value_string"]'),
            'value_int': row.querySelector('div[id$="-value_int"]'),
            'value_bool': row.querySelector('div[id$="-value_bool"]'),
            'value_date': row.querySelector('div[id$="-value_date"]'),
            'value_url': row.querySelector('div[id$="-value_url"]')
        };

        function toggleFields() {
            const selectedText = typeSelect.options[typeSelect.selectedIndex].text.toLowerCase();
            Object.values(fields).forEach(f => { if(f) f.classList.add('d-none') });

            if (selectedText.includes('string')) fields.value_string?.classList.remove('d-none');
            else if (selectedText.includes('integer')) fields.value_int?.classList.remove('d-none');
            else if (selectedText.includes('bool')) fields.value_bool?.classList.remove('d-none');
            else if (selectedText.includes('date')) fields.value_date?.classList.remove('d-none');
            else if (selectedText.includes('url')) fields.value_url?.classList.remove('d-none');
        }

        typeSelect.addEventListener('change', toggleFields);
        toggleFields();

        const delCheck = row.querySelector('input[name$="-DELETE"]');
        if (delCheck) {
            delCheck.addEventListener('change', () => {
                row.style.opacity = delCheck.checked ? "0.4" : "1";
                row.style.filter = delCheck.checked ? "grayscale(1)" : "none";
            });
        }
    }

    // Initialize existing rows
    document.querySelectorAll('.attribute-row').forEach(row => setupVisibility(row));

    // --- 3. Profile Picture Preview Logic ---
    const fileInput = document.querySelector('#id_profile_pic');
    const previewImg = document.querySelector('#profile-pic-preview');
    const removeSelectionBtn = document.querySelector('#remove-pic-btn'); // For newly picked files
    const deleteExistingBtn = document.querySelector('#delete-existing-pic'); // For DB files
    const clearFlag = document.querySelector('#clear-image-flag');
    
    // Store original states
    const originalSrc = previewImg ? previewImg.src : "";
    const defaultAvatar = previewImg ? previewImg.getAttribute('data-default') : "";

    if (fileInput && previewImg) {
        
        // A. Handling NEW file selection from computer
        fileInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    previewImg.src = e.target.result;
                    previewImg.classList.remove('d-none'); 
                    
                    if (removeSelectionBtn) removeSelectionBtn.classList.remove('d-none');
                    if (deleteExistingBtn) deleteExistingBtn.classList.add('d-none'); // Hide delete while picking new
                    if (clearFlag) clearFlag.value = "false"; // Reset the deletion flag
                };
                reader.readAsDataURL(file);
            }
        });

        // B. "Cancel Selection" Button (Undo a fresh file pick)
        if (removeSelectionBtn) {
            removeSelectionBtn.addEventListener('click', function() {
                fileInput.value = ""; 
                removeSelectionBtn.classList.add('d-none');
                
                // Revert to original database image or default
                if (originalSrc && !originalSrc.includes('default-avatar.png')) {
                    previewImg.src = originalSrc;
                    if (deleteExistingBtn) deleteExistingBtn.classList.remove('d-none');
                } else {
                    previewImg.src = defaultAvatar;
                }
                
                if (clearFlag) clearFlag.value = "false";
            });
        }

        // C. "Remove Photo" Button (Delete existing from Database)
        if (deleteExistingBtn) {
            deleteExistingBtn.addEventListener('click', function() {
                if (confirm("Are you sure you want to remove your profile picture?")) {
                    // Update visual to default
                    previewImg.src = defaultAvatar;
                    
                    // Set the hidden flag for Django
                    if (clearFlag) clearFlag.value = "true";
                    
                    // UI Cleanup
                    deleteExistingBtn.classList.add('d-none');
                    fileInput.value = ""; // Clear any pending file selection
                    if (removeSelectionBtn) removeSelectionBtn.classList.add('d-none');
                }
            });
        }
    }
});

