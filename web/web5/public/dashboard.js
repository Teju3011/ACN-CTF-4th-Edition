// Dashboard functionality

document.addEventListener('DOMContentLoaded', function() {
    // Check if user is authenticated
    const authCookie = document.cookie
        .split('; ')
        .find(row => row.startsWith('auth='));
    
    if (!authCookie) {
        window.location.href = '/';
        return;
    }
    
    // Add subtle hints to the console for CTF players
    console.log('TechCorp Employee Portal - Session Management System');
    console.log('Session data is stored in browser cookies for quick access');
    
    // Decode and log session info (for educational purposes in CTF)
    try {
        const decoded = atob(authCookie.split('=')[1]);
        console.log('Current session data format: JSON encoded in Base64');
        console.log('Session structure example: {"user":"username","role":"user"}');
        
        // Only show this hint if user is not already admin
        const sessionData = JSON.parse(decoded);
        if (sessionData.role !== 'admin') {
            console.log('Note: Administrative functions require elevated privileges');
            console.log('Tip: Examine how the application determines user roles...');
        }
    } catch (e) {
        console.log('Unable to parse session data');
    }
    
    // Update navigation with user info
    updateUserNavigation();
});

function updateUserNavigation() {
    const authCookie = document.cookie
        .split('; ')
        .find(row => row.startsWith('auth='));
    
    if (authCookie) {
        try {
            const decoded = atob(authCookie.split('=')[1]);
            const userData = JSON.parse(decoded);
            
            const userInfoElement = document.getElementById('userInfo');
            if (userInfoElement) {
                userInfoElement.textContent = `${userData.user} (${userData.role})`;
            }
            
            // Update dashboard header based on role
            const dashboardHeader = document.querySelector('.dashboard-header h1');
            if (dashboardHeader && userData.role === 'admin') {
                dashboardHeader.textContent = 'Administrator Dashboard';
            }
        } catch (e) {
            console.log('Error parsing user session');
        }
    }
}

function logout() {
    // Clear the auth cookie
    document.cookie = 'auth=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
    window.location.href = '/';
}

// Add some interactivity to disabled buttons
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('disabled')) {
        e.preventDefault();
        
        // Show a tooltip or message for disabled features
        const tooltip = document.createElement('div');
        tooltip.textContent = 'Feature not available with current access level';
        tooltip.style.position = 'absolute';
        tooltip.style.background = '#2d3748';
        tooltip.style.color = 'white';
        tooltip.style.padding = '8px 12px';
        tooltip.style.borderRadius = '6px';
        tooltip.style.fontSize = '14px';
        tooltip.style.zIndex = '1000';
        tooltip.style.pointerEvents = 'none';
        
        const rect = e.target.getBoundingClientRect();
        tooltip.style.left = rect.left + 'px';
        tooltip.style.top = (rect.top - 40) + 'px';
        
        document.body.appendChild(tooltip);
        
        setTimeout(() => {
            document.body.removeChild(tooltip);
        }, 2000);
    }
});
