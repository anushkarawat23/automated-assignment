

// JavaScript to enhance file input experience or show feedback
document.getElementById('file').addEventListener('change', function() {
    const fileList = this.files;
    const feedback = document.getElementById('feedback');
    
    if (fileList.length > 0) {
        feedback.textContent = `You have selected ${fileList.length} file(s). Ready to upload!`;
    } else {
        feedback.textContent = '';
    }
});


