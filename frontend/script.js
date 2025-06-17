document.addEventListener('DOMContentLoaded', function() {
    const serverButtons = document.querySelectorAll('.btn-danger');
    
    serverButtons.forEach(button => {
        button.addEventListener('click', async function() {
            const card = this.closest('.card');
            const serverType = card.querySelector('.card-title').textContent;
            const hasNgrok = card.querySelector('.ngrok-badge') !== null;
            
            // Change button state to loading
            const originalText = this.textContent;
            this.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Launching...';
            this.disabled = true;
            
            try {
                // Simulate server launch (replace with actual server launch logic)
                await new Promise(resolve => setTimeout(resolve, 2000));
                
                // Show success message
                this.innerHTML = '<i class="fas fa-check"></i> Running';
                this.classList.remove('btn-danger');
                this.classList.add('btn-success');
                
                // Add running indicator
                const statusBadge = document.createElement('span');
                statusBadge.className = 'status-badge running-badge';
                statusBadge.innerHTML = '<i class="fas fa-circle"></i> Running';
                card.querySelector('.card-body').appendChild(statusBadge);
                
            } catch (error) {
                // Show error state
                this.innerHTML = '<i class="fas fa-times"></i> Failed';
                this.classList.remove('btn-danger');
                this.classList.add('btn-secondary');
            }
        });
    });
}); 