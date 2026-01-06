// Custom admin JavaScript for better UX

(function() {
    'use strict';
    
    // Wait for DOM to load
    document.addEventListener('DOMContentLoaded', function() {
        
        // Auto-hide fields based on content type selection
        const contentTypeSelects = document.querySelectorAll('select[name*="content_type"]');
        
        contentTypeSelects.forEach(function(select) {
            function updateVisibility() {
                const inline = select.closest('.inline-related');
                if (!inline) return;
                
                const contentType = select.value;
                
                // Get all field rows
                const textRow = inline.querySelector('.field-text_content');
                const imageRow = inline.querySelector('.field-image');
                const captionRow = inline.querySelector('.field-image_caption');
                const quoteRow = inline.querySelector('.field-quote_text');
                const authorRow = inline.querySelector('.field-quote_author');
                const codeRow = inline.querySelector('.field-code_content');
                const langRow = inline.querySelector('.field-code_language');
                
                // Hide all
                [textRow, imageRow, captionRow, quoteRow, authorRow, codeRow, langRow].forEach(row => {
                    if (row) row.style.display = 'none';
                });
                
                // Show relevant fields
                if (contentType === 'text' && textRow) {
                    textRow.style.display = 'block';
                }
                else if (contentType === 'image') {
                    if (imageRow) imageRow.style.display = 'block';
                    if (captionRow) captionRow.style.display = 'block';
                }
                else if (contentType === 'quote') {
                    if (quoteRow) quoteRow.style.display = 'block';
                    if (authorRow) authorRow.style.display = 'block';
                }
                else if (contentType === 'code') {
                    if (codeRow) codeRow.style.display = 'block';
                    if (langRow) langRow.style.display = 'block';
                }
            }
            
            // Run on load
            updateVisibility();
            
            // Run on change
            select.addEventListener('change', updateVisibility);
        });
        
        // Add confirmation for delete
        const deleteCheckboxes = document.querySelectorAll('input[name*="DELETE"]');
        deleteCheckboxes.forEach(function(checkbox) {
            checkbox.addEventListener('change', function() {
                if (this.checked) {
                    if (!confirm('Are you sure you want to delete this content block?')) {
                        this.checked = false;
                    }
                }
            });
        });
    });
})();