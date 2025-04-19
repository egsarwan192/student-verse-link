
/**
 * Campus Connect Main JavaScript
 * Handles user interactions including role selection and form submission
 */

document.addEventListener('DOMContentLoaded', function() {
    // Role selection toggle handling
    const roleInputs = document.querySelectorAll('input[name="role"]');
    if (roleInputs.length) {
        roleInputs.forEach(input => {
            input.addEventListener('change', function() {
                // Add visual feedback when role is selected
                document.getElementById('selected-role').textContent = this.value.charAt(0).toUpperCase() + this.value.slice(1);
            });
        });
    }

    // Form validation for login
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(event) {
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const roleChecked = document.querySelector('input[name="role"]:checked');
            
            let isValid = true;
            
            // Basic validation
            if (!email || !validateEmail(email)) {
                showError('email-error', 'Please enter a valid email address');
                isValid = false;
            } else {
                clearError('email-error');
            }
            
            if (!password) {
                showError('password-error', 'Password is required');
                isValid = false;
            } else {
                clearError('password-error');
            }
            
            if (!roleChecked) {
                showError('role-error', 'Please select a role');
                isValid = false;
            } else {
                clearError('role-error');
            }
            
            if (!isValid) {
                event.preventDefault();
            }
        });
    }
    
    // Form validation for signup
    const signupForm = document.getElementById('signup-form');
    if (signupForm) {
        signupForm.addEventListener('submit', function(event) {
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const confirmPassword = document.getElementById('confirm-password').value;
            const roleChecked = document.querySelector('input[name="role"]:checked');
            
            let isValid = true;
            
            // Basic validation
            if (!email || !validateEmail(email)) {
                showError('email-error', 'Please enter a valid email address');
                isValid = false;
            } else {
                clearError('email-error');
            }
            
            if (!password || password.length < 8) {
                showError('password-error', 'Password must be at least 8 characters');
                isValid = false;
            } else {
                clearError('password-error');
            }
            
            if (password !== confirmPassword) {
                showError('confirm-password-error', 'Passwords do not match');
                isValid = false;
            } else {
                clearError('confirm-password-error');
            }
            
            if (!roleChecked) {
                showError('role-error', 'Please select a role');
                isValid = false;
            } else {
                clearError('role-error');
            }
            
            if (!isValid) {
                event.preventDefault();
            }
        });
    }
    
    // Add animation to CTA buttons
    const ctaButtons = document.querySelectorAll('.btn');
    ctaButtons.forEach(button => {
        button.addEventListener('mouseover', function() {
            this.style.transition = 'all 0.3s ease';
        });
    });
});

// Helper functions
function validateEmail(email) {
    const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
}

function showError(elementId, message) {
    const errorElement = document.getElementById(elementId);
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }
}

function clearError(elementId) {
    const errorElement = document.getElementById(elementId);
    if (errorElement) {
        errorElement.textContent = '';
        errorElement.style.display = 'none';
    }
}
