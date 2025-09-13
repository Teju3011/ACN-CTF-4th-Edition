// TechCorp Portal - Utility Functions

// Subtle development logging for security analysis
if (window.console) {
    console.log('TechCorp Employee Portal v2.1.4');
    console.log('Session management: Cookie-based authentication');
    console.log('For technical support, contact: it-support@techcorp.com');
}

// Session validation utility
function validateSession() {
    const authCookie = document.cookie
        .split('; ')
        .find(row => row.startsWith('auth='));
    
    if (!authCookie) {
        console.log('No active session found');
        return false;
    }
    
    try {
        const sessionData = atob(authCookie.split('=')[1]);
        console.log('Session format: Base64-encoded JSON');
        return true;
    } catch (e) {
        console.log('Invalid session format detected');
        return false;
    }
}

// Development utilities (for debugging)
window.debugUtils = {
    decodeSession: function() {
        const authCookie = document.cookie
            .split('; ')
            .find(row => row.startsWith('auth='));
        
        if (authCookie) {
            try {
                const decoded = atob(authCookie.split('=')[1]);
                console.log('Current session:', decoded);
                return JSON.parse(decoded);
            } catch (e) {
                console.log('Failed to decode session');
            }
        }
        return null;
    },
    
    showCookies: function() {
        console.log('Browser cookies:', document.cookie);
    }
};

// Initialize session validation on load
document.addEventListener('DOMContentLoaded', validateSession);
