
// Auction Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // If we're on the auction page, load the auctions
    if (document.getElementById('auctionItems')) {
        loadAuctions();
        
        // Set minimum date for end date to today
        const today = new Date();
        const todayFormatted = today.toISOString().split('T')[0];
        document.getElementById('endDate').min = todayFormatted;
        
        // Form validation for new auction
        const newAuctionForm = document.getElementById('newAuctionForm');
        newAuctionForm.addEventListener('submit', function(event) {
            event.preventDefault();
            if (!newAuctionForm.checkValidity()) {
                event.stopPropagation();
                newAuctionForm.classList.add('was-validated');
                return;
            }
            
            // Submit new auction
            const auctionData = {
                title: document.getElementById('title').value,
                description: document.getElementById('description').value,
                starting_price: parseFloat(document.getElementById('startingPrice').value),
                end_date: document.getElementById('endDate').value
            };
            
            fetch('/api/auctions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(auctionData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Show success message
                    showToast('Auction created successfully!', 'success');
                    
                    // Reset form
                    newAuctionForm.reset();
                    newAuctionForm.classList.remove('was-validated');
                    
                    // Reload auctions
                    loadAuctions();
                } else {
                    // Show error message
                    showToast(`Error: ${data.message}`, 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showToast('Error creating auction. Please try again.', 'danger');
            });
        });
        
        // Setup bid form handler
        const placeBidBtn = document.getElementById('placeBidBtn');
        placeBidBtn.addEventListener('click', function() {
            const bidForm = document.getElementById('bidForm');
            if (!bidForm.checkValidity()) {
                bidForm.classList.add('was-validated');
                return;
            }
            
            const auctionId = document.getElementById('auctionId').value;
            const bidAmount = parseFloat(document.getElementById('bidAmount').value);
            const currentBid = parseFloat(document.getElementById('currentBid').value);
            
            if (bidAmount <= currentBid) {
                const bidInput = document.getElementById('bidAmount');
                bidInput.setCustomValidity('Bid must be higher than current bid');
                bidForm.classList.add('was-validated');
                return;
            }
            
            // Submit bid
            fetch(`/api/auctions/${auctionId}/bid`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ bid_amount: bidAmount })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    // Close modal
                    const bidModal = bootstrap.Modal.getInstance(document.getElementById('bidModal'));
                    bidModal.hide();
                    
                    // Reload auctions
                    loadAuctions();
                    
                    // Show success toast
                    showToast('Bid placed successfully!', 'success');
                } else {
                    // Show error message
                    showToast(`Error: ${data.message}`, 'danger');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showToast('Error placing bid. Please try again.', 'danger');
            });
        });
    }
});

// Load auctions from API
function loadAuctions() {
    const auctionItems = document.getElementById('auctionItems');
    auctionItems.innerHTML = `
        <div class="col-12 text-center">
            <div class="spinner-border" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>
    `;
    
    fetch('/api/auctions')
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                if (data.data.length === 0) {
                    auctionItems.innerHTML = `
                        <div class="col-12 text-center">
                            <p>No auctions available at the moment.</p>
                            <p>Create a new auction to get started!</p>
                        </div>
                    `;
                    return;
                }
                
                auctionItems.innerHTML = '';
                data.data.forEach(auction => {
                    const endDate = new Date(auction.end_date);
                    const now = new Date();
                    const isActive = auction.status === 'active' && endDate > now;
                    
                    const auctionCard = document.createElement('div');
                    auctionCard.className = 'col-md-4 mb-4';
                    auctionCard.innerHTML = `
                        <div class="card h-100">
                            <div class="card-header d-flex justify-content-between align-items-center">
                                <span class="badge ${isActive ? 'bg-success' : 'bg-danger'}">
                                    ${isActive ? 'Active' : 'Closed'}
                                </span>
                                <span>Ends: ${formatDate(auction.end_date)}</span>
                            </div>
                            <div class="card-body d-flex flex-column">
                                <h5 class="card-title">${auction.title}</h5>
                                <p class="card-text">${auction.description}</p>
                                <div class="mt-auto">
                                    <div class="d-flex justify-content-between align-items-center mb-3">
                                        <span>Current Bid:</span>
                                        <span class="fw-bold">$${auction.current_price.toFixed(2)}</span>
                                    </div>
                                    <div class="d-grid gap-2">
                                        <button class="btn btn-primary ${!isActive ? 'disabled' : ''}" 
                                            ${!isActive ? 'disabled' : ''}
                                            onclick="openBidModal('${auction.id}', ${auction.current_price})">
                                            Place Bid
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                    auctionItems.appendChild(auctionCard);
                });
            } else {
                auctionItems.innerHTML = `
                    <div class="col-12">
                        <div class="alert alert-danger" role="alert">
                            Error loading auctions. Please try again later.
                        </div>
                    </div>
                `;
            }
        })
        .catch(error => {
            console.error('Error:', error);
            auctionItems.innerHTML = `
                <div class="col-12">
                    <div class="alert alert-danger" role="alert">
                        Error loading auctions. Please try again later.
                    </div>
                </div>
            `;
        });
}

// Format date for display
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

// Open bid modal
function openBidModal(auctionId, currentPrice) {
    document.getElementById('auctionId').value = auctionId;
    document.getElementById('currentBid').value = currentPrice.toFixed(2);
    document.getElementById('bidAmount').value = (currentPrice + 1).toFixed(2);
    document.getElementById('bidAmount').min = currentPrice + 0.01;
    
    // Reset validation
    const bidForm = document.getElementById('bidForm');
    bidForm.classList.remove('was-validated');
    document.getElementById('bidAmount').setCustomValidity('');
    
    const bidModal = new bootstrap.Modal(document.getElementById('bidModal'));
    bidModal.show();
}

// Show toast message
function showToast(message, type) {
    // Create toast container if it doesn't exist
    let toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
        toastContainer = document.createElement('div');
        toastContainer.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        document.body.appendChild(toastContainer);
    }
    
    // Create toast
    const toastId = 'toast-' + Date.now();
    const toast = document.createElement('div');
    toast.className = `toast bg-${type} text-white`;
    toast.setAttribute('id', toastId);
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    toast.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">
                ${message}
            </div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
    `;
    
    toastContainer.appendChild(toast);
    
    // Show toast
    const bsToast = new bootstrap.Toast(toast, { autohide: true, delay: 3000 });
    bsToast.show();
    
    // Remove toast after it's hidden
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}
