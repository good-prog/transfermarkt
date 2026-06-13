document.addEventListener('DOMContentLoaded', () => {

    const editProfileBtn = document.getElementById('editProfileBtn');
    const saveProfileBtn = document.getElementById('saveProfileBtn');
    const subPositionDisplay = document.getElementById('subPositionDisplay');
    const playerContext = document.getElementById('playerContext');

    // Acquire tracking database record index cleanly from model wrapper definitions
    const playerId = playerContext.getAttribute('data-id');
    const editableElements = document.querySelectorAll('[data-editable]');
    let dataCache = {};

    // --- STATE TRANSLATION TO SYSTEM INPUT ACTIVE FORM ---
    editProfileBtn.addEventListener('click', () => {
        editProfileBtn.classList.add('hidden');
        saveProfileBtn.classList.remove('hidden');

        editableElements.forEach(element => {
            const fieldKey = element.getAttribute('data-editable');
            let baseTextValue = "";

            // Extract core image routing strings cleanly if tracking specific visual targets
            if (fieldKey === 'photoUrl' || fieldKey === 'logoUrl') {
                const innerImg = element.querySelector('img');
                baseTextValue = innerImg ? innerImg.getAttribute('src') : "";
            } else {
                baseTextValue = element.innerText || element.textContent;
            }

            dataCache[fieldKey] = baseTextValue;

            // Generate structural interactive text element components 
            const textfield = document.createElement('input');
            textfield.type = 'text';
            textfield.className = 'inline-edit-input';
            textfield.value = baseTextValue.trim();
            textfield.placeholder = `Update ${fieldKey} path`;

            element.innerHTML = '';
            element.appendChild(textfield);
        });
    });

    // --- BACKEND RECONCILIATION SUBMIT SAVE COMMIT ---
    saveProfileBtn.addEventListener('click', () => {
        saveProfileBtn.classList.add('hidden');
        editProfileBtn.classList.remove('hidden');

        editableElements.forEach(element => {
            const fieldKey = element.getAttribute('data-editable');
            const targetInput = element.querySelector('.inline-edit-input');

            if (targetInput) {
                let textValue = targetInput.value.trim();
                dataCache[fieldKey] = textValue;

                // Reconstruct visual DOM layers cleanly with fallback icons preserved securely
                if (fieldKey === 'photoUrl') {
                    element.innerHTML = textValue ? `<img src="${textValue}" class="player-profile-img">` : '<div class="player-photo-placeholder"><i class="fa-solid fa-user-tie"></i></div>';
                } else if (fieldKey === 'logoUrl') {
                    element.innerHTML = textValue ? `<img src="${textValue}" class="club-badge-img">` : '';
                } else if (fieldKey === 'featuredPhotoUrl') {
                    // ADD THIS CONDITIONAL BLOCK FOR THE NEW IMAGE
                    element.innerHTML = textValue ? `<img src="${textValue}" class="gallery-main-img">` : '<div class="gallery-empty-state"><i class="fa-solid fa-image-portrait"></i><p>No imagery loaded</p></div>';
                } else {
                    element.textContent = textValue;
                }
            }
        });

        // Mirror text variables across subordinate content layouts
        if (dataCache['position'] && subPositionDisplay) {
            subPositionDisplay.textContent = dataCache['position'];
        }

        // --- FETCH REST TRANSMISSION STREAM SUBMIT TO LOCAL SQL SERVER ---
        fetch(`/player/${playerId}/update`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dataCache)
        })
            .then(res => res.json())
            .then(response => {
                console.log("Database Sync completed securely payload returned:", response);
            })
            .catch(err => {
                alert("Network connection drop timed out. Synchronization halted.");
                console.error("Fetch Exception intercept caught:", err);
            });
    });
});
