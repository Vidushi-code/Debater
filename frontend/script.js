// ===================================
// DOM Elements
// ===================================
const analyzeBtn = document.getElementById('analyzeBtn');
const ideaInput = document.getElementById('ideaInput');
const agentOutputsSection = document.getElementById('agentOutputs');

// Output elements
const goodAgentOutput = document.getElementById('goodAgentOutput');
const devilAgentOutput = document.getElementById('devilAgentOutput');
const researchAgentOutput = document.getElementById('researchAgentOutput');
const conversationalAgentOutput = document.getElementById('conversationalAgentOutput');
const finalConclusionOutput = document.getElementById('finalConclusionOutput');

// ===================================
// Mock Backend Function
// ===================================
/**
 * Simulates backend API call to get agent outputs
 * @param {string} userInput - The user's idea description
 * @returns {Object} - Contains outputs from all agents
 */
async function getAgentOutputs(userInput) {
    try {
        const response = await fetch('http://localhost:8001/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ idea: userInput })
        });

        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }

        const data = await response.json();

        // Handle chat-only response
        if (data.type === 'chat') {
            return {
                conversationalAgent: data.conversationalAgent,
                // Empty others to hide them or show specific state
                goodAgent: '',
                devilAgent: '',
                researchAgent: '',
                finalConclusion: ''
            };
        }

        return data;
    } catch (error) {
        console.error('API Error:', error);
        // Show error to user
        const btn = document.getElementById('analyzeBtn');
        const originalText = btn.innerHTML;
        btn.innerHTML = `<i class="fas fa-exclamation-circle"></i> Error: ${error.message}`;
        btn.style.background = '#ef4444';

        setTimeout(() => {
            btn.innerHTML = originalText;
            btn.style.background = '';
            btn.disabled = false;
        }, 3000);

        throw error;
    }
}

// ===================================
// Event Listeners
// ===================================
analyzeBtn.addEventListener('click', handleAnalyze);

// Allow Enter key to submit (Ctrl+Enter for new line)
ideaInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey && !e.ctrlKey) {
        e.preventDefault();
        handleAnalyze();
    }
});

// ===================================
// Main Analysis Handler
// ===================================
/**
 * Handles the analysis process when user clicks the analyze button
 */
async function handleAnalyze() {
    const userInput = ideaInput.value.trim();

    // Validation
    if (!userInput) {
        showNotification('Please describe your idea first!', 'error');
        ideaInput.focus();
        return;
    }

    // Validation
    if (!userInput) {
        showNotification('Please describe your idea first!', 'error');
        ideaInput.focus();
        return;
    }

    // Removed length check to allow for chat interactions (e.g., "Hello")
    // The backend Intent Classifier will handle short inputs.

    // Disable button and show loading state
    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Thinking...';

    // Hide "How It Works" to focus on the interaction
    document.getElementById('how-it-works').style.display = 'none';

    try {
        // 1. Classify Intent
        const classifyResponse = await fetch('http://localhost:8001/classify', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ idea: userInput })
        });
        const classification = await classifyResponse.json();

        if (classification.type === 'chat') {
            // 2a. Chat Mode
            // Show user message immediately
            appendMessage(userInput, 'user');

            // Clear input immediately for better UX
            ideaInput.value = '';

            const chatResponse = await fetch('http://localhost:8001/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ idea: userInput })
            });
            const chatData = await chatResponse.json();

            appendMessage(chatData.response, 'agent');

        } else {
            // 2b. Analysis Mode
            analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';

            const analyzeResponse = await fetch('http://localhost:8001/analyze', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ idea: userInput })
            });
            const analysisData = await analyzeResponse.json();

            displayAnalysis(analysisData);
            showNotification('Analysis complete!', 'success');
        }

    } catch (error) {
        console.error('Operation failed:', error);
        showNotification('Something went wrong. Please try again.', 'error');
    } finally {
        // Reset button
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = '<i class="fas fa-magic"></i> Analyze Idea';
    }
}

function appendMessage(text, sender) {
    // Ensure chat section is visible
    agentOutputsSection.classList.remove('active');
    const chatSection = document.getElementById('chatSection');
    chatSection.classList.add('active');

    const history = document.getElementById('chatHistory');
    const bubble = document.createElement('div');
    bubble.className = `message message-${sender}`;
    bubble.textContent = text;

    history.appendChild(bubble);

    // Scroll to bottom
    history.scrollTop = history.scrollHeight;

    // Scroll section into view if needed (only on first message)
    if (history.children.length <= 2) {
        setTimeout(() => {
            chatSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 300);
    }
}

function displayAnalysis(outputs) {
    // Hide chat, show analysis
    document.getElementById('chatSection').classList.remove('active');
    displayResults(outputs); // Existing function
}

// ===================================
// Display Results
// ===================================
/**
 * Displays the agent outputs in their respective cards
 * @param {Object} outputs - Contains all agent outputs
 */
function displayResults(outputs) {
    // Clear previous results and reset animations
    agentOutputsSection.classList.remove('active');
    clearOutputs();

    // Small delay to allow DOM to reset
    setTimeout(() => {
        // Populate outputs
        goodAgentOutput.textContent = outputs.goodAgent;
        devilAgentOutput.textContent = outputs.devilAgent;
        researchAgentOutput.textContent = outputs.researchAgent;
        conversationalAgentOutput.textContent = outputs.conversationalAgent;
        finalConclusionOutput.textContent = outputs.finalConclusion;

        // Show section with animations
        agentOutputsSection.classList.add('active');
    }, 100);
}

// ===================================
// Helper Functions
// ===================================
/**
 * Clears all output fields
 */
function clearOutputs() {
    goodAgentOutput.textContent = '';
    devilAgentOutput.textContent = '';
    researchAgentOutput.textContent = '';
    conversationalAgentOutput.textContent = '';
    finalConclusionOutput.textContent = '';
}

/**
 * Shows a notification message to the user
 * @param {string} message - The message to display
 * @param {string} type - Type of notification (success, error, warning)
 */
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <i class="fas fa-${getNotificationIcon(type)}"></i>
        <span>${message}</span>
    `;

    // Add styles
    Object.assign(notification.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        padding: '15px 25px',
        background: getNotificationColor(type),
        color: 'white',
        borderRadius: '10px',
        boxShadow: '0 4px 15px rgba(0, 0, 0, 0.2)',
        zIndex: '10000',
        display: 'flex',
        alignItems: 'center',
        gap: '10px',
        animation: 'slideInRight 0.3s ease',
        fontWeight: '500'
    });

    // Append to body
    document.body.appendChild(notification);

    // Remove after 3 seconds
    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

/**
 * Gets the appropriate icon for notification type
 * @param {string} type - Notification type
 * @returns {string} - Font Awesome icon name
 */
function getNotificationIcon(type) {
    const icons = {
        success: 'check-circle',
        error: 'exclamation-circle',
        warning: 'exclamation-triangle',
        info: 'info-circle'
    };
    return icons[type] || icons.info;
}

/**
 * Gets the appropriate color for notification type
 * @param {string} type - Notification type
 * @returns {string} - CSS color value
 */
function getNotificationColor(type) {
    const colors = {
        success: '#10b981',
        error: '#ef4444',
        warning: '#f59e0b',
        info: '#3b82f6'
    };
    return colors[type] || colors.info;
}

// ===================================
// Smooth Scrolling for Navigation
// ===================================
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// ===================================
// Add CSS animations dynamically
// ===================================
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// ===================================
// Console Welcome Message
// ===================================
console.log('%c🔮 Multi-Perspective AI Analyst', 'color: #6366f1; font-size: 20px; font-weight: bold;');
console.log('%cReady to analyze your ideas!', 'color: #8b5cf6; font-size: 14px;');
console.log('%cBackend API integration point: getAgentOutputs()', 'color: #10b981; font-size: 12px;');
