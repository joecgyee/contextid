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
    const removeBtn = document.querySelector('#remove-pic-btn');
    
    // Store the initial source (if editing an existing profile)
    const originalSrc = previewImg ? previewImg.src : "";

    if (fileInput && previewImg) {
        fileInput.addEventListener('change', function(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    previewImg.src = e.target.result;
                    previewImg.classList.remove('d-none'); 
                    if (removeBtn) removeBtn.classList.remove('d-none');
                };
                reader.readAsDataURL(file);
            }
        });

        if (removeBtn) {
            removeBtn.addEventListener('click', function() {
                fileInput.value = ""; 
                // If there was an original image, go back to it. Otherwise hide.
                if (originalSrc && !originalSrc.endsWith('#')) {
                    previewImg.src = originalSrc;
                } else {
                    previewImg.src = "#";
                    previewImg.classList.add('d-none');
                }
                removeBtn.classList.add('d-none');
            });
        }
    }
});

