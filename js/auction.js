
// Auction Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // If we're on the auction page, load the auctions
    if (document.getElementById('auctionItems')) {
        loadAuctions();
    }
});

// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    }).format(date);
}

// Calculate time remaining
function getTimeRemaining(endTime) {
    const total = Date.parse(endTime) - Date.parse(new Date());
    const seconds = Math.floor((total / 1000) % 60);
    const minutes = Math.floor((total / 1000 / 60) % 60);
    const hours = Math.floor((total / (1000 * 60 * 60)) % 24);
    const days = Math.floor(total / (1000 * 60 * 60 * 24));
    
    return {
        total,
        days,
        hours,
        minutes,
        seconds
    };
}

// Format time remaining
function formatTimeRemaining(timeRemaining) {
    if (timeRemaining.total <= 0) {
        return 'Auction ended';
    }
    
    if (timeRemaining.days > 0) {
        return `${timeRemaining.days}d ${timeRemaining.hours}h remaining`;
    }
    
    if (timeRemaining.hours > 0) {
        return `${timeRemaining.hours}h ${timeRemaining.minutes}m remaining`;
    }
    
    return `${timeRemaining.minutes}m ${timeRemaining.seconds}s remaining`;
}
