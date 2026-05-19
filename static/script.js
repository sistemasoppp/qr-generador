document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('qr-form');
    const urlInput = document.getElementById('url');
    const submitBtn = document.getElementById('generate-btn');
    const btnText = submitBtn.querySelector('.btn-text');
    const spinner = document.getElementById('loading-spinner');
    const resultContainer = document.getElementById('result-container');
    const qrImage = document.getElementById('qr-image');
    const downloadBtn = document.getElementById('download-btn');

    let currentBlobUrl = null;

    const logoInput = document.getElementById('logo');
    const fileNameDisplay = document.getElementById('file-name');

    // Update file name display when a file is selected
    logoInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            fileNameDisplay.textContent = e.target.files[0].name;
        } else {
            fileNameDisplay.textContent = 'Seleccionar archivo...';
        }
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const urlValue = urlInput.value.trim();
        if (!urlValue) return;

        // Set Loading State
        btnText.classList.add('hidden');
        spinner.classList.remove('hidden');
        submitBtn.disabled = true;
        resultContainer.classList.add('hidden');

        try {
            const formData = new FormData();
            formData.append('url', urlValue);
            if (logoInput.files.length > 0) {
                formData.append('logo', logoInput.files[0]);
            }

            const response = await fetch('/generar', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Error al generar el QR');
            }

            // Get image blob
            const blob = await response.blob();
            
            // Create object URL
            if (currentBlobUrl) {
                URL.revokeObjectURL(currentBlobUrl);
            }
            currentBlobUrl = URL.createObjectURL(blob);
            
            // Display Image
            qrImage.src = currentBlobUrl;
            
            // Show result container
            resultContainer.classList.remove('hidden');

        } catch (error) {
            alert(error.message);
            console.error(error);
        } finally {
            // Reset Loading State
            btnText.classList.remove('hidden');
            spinner.classList.add('hidden');
            submitBtn.disabled = false;
        }
    });

    downloadBtn.addEventListener('click', () => {
        if (!currentBlobUrl) return;
        
        const a = document.createElement('a');
        a.href = currentBlobUrl;
        a.download = 'qr_institucional.png';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    });
});
