document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('fileInput');
    const cameraBtn = document.getElementById('cameraBtn');
    
    // Sections
    const uploadSection = document.getElementById('uploadSection');
    const loadingSection = document.getElementById('loadingSection');
    const resultsSection = document.getElementById('resultsSection');
    
    // Results DOM
    const scannerPreview = document.getElementById('scannerPreview');
    const bookList = document.getElementById('bookList');
    const bookCount = document.getElementById('bookCount');
    const resetBtn = document.getElementById('resetBtn');
    const exportBtn = document.getElementById('exportBtn');

    // Drag & Drop handlers
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.add('dragover'), false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, () => dropZone.classList.remove('dragover'), false);
    });

    dropZone.addEventListener('drop', (e) => {
        let files = e.dataTransfer.files;
        if (files.length > 0) handleFile(files[0]);
    });

    fileInput.addEventListener('change', function() {
        if (this.files.length > 0) handleFile(this.files[0]);
    });

    // Handle File Selection
    function handleFile(file) {
        if (!file.type.startsWith('image/')) {
            alert('Please upload an image file.');
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            startProcessing(file, e.target.result);
        };
        reader.readAsDataURL(file);
    }

    // Real API Process
    async function startProcessing(file, imageSrc) {
        uploadSection.classList.add('hidden');
        loadingSection.classList.remove('hidden');
        
        scannerPreview.style.backgroundImage = `url(${imageSrc})`;

        const formData = new FormData();
        formData.append('image', file);

        try {
            const response = await fetch('http://localhost:5001/api/scan-bookshelf', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Server error occurred');
            }

            const data = await response.json();
            showResults(data.books);
        } catch (error) {
            console.error('Error scanning bookshelf:', error);
            alert('Error scanning bookshelf: ' + error.message + '\n\nDid you start the Python server and set your GEMINI_API_KEY?');
            resetBtn.click();
        }
    }

    // Show real results
    function showResults(books) {
        loadingSection.classList.add('hidden');
        resultsSection.classList.remove('hidden');

        bookCount.textContent = `${books.length} Books`;
        bookList.innerHTML = '';

        books.forEach(book => {
            const li = document.createElement('li');
            li.className = 'book-item';
            li.innerHTML = `
                <div class="book-icon"><i class="ph ph-book-open"></i></div>
                <div class="book-info">
                    <h3>${book.title}</h3>
                    <p>${book.author}</p>
                </div>
            `;
            bookList.appendChild(li);
        });
    }

    // Reset Flow
    resetBtn.addEventListener('click', () => {
        resultsSection.classList.add('hidden');
        uploadSection.classList.remove('hidden');
        fileInput.value = '';
    });
    
    // Future expansion: Camera support
    cameraBtn.addEventListener('click', () => {
        alert("Camera integration component will open here.");
    });
});
