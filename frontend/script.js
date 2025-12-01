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
function getAgentOutputs(userInput) {
    // Simulate API delay
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve({
                goodAgent: `✨ Excellent idea! "${userInput.substring(0, 50)}..." shows great potential.\n\nPositive aspects:\n• Addresses a real market need\n• Has scalable potential\n• Aligns with current trends\n• Could generate multiple revenue streams\n\nThis concept demonstrates innovation and forward-thinking. With proper execution, it could become a market leader in its category.`,
                
                devilAgent: `⚠️ Critical Analysis:\n\nWhile the idea "${userInput.substring(0, 50)}..." has merit, several challenges need addressing:\n\n• Market saturation - Similar solutions already exist\n• High initial capital requirement\n• Steep learning curve for target users\n• Regulatory hurdles may slow implementation\n• Customer acquisition costs could be prohibitive\n\nRecommendation: Conduct thorough feasibility study before proceeding.`,
                
                researchAgent: `📈 Market Research Insights:\n\nBased on historical data and current trends:\n\n• Market size: Growing at 15-20% annually\n• Competition: 12+ established players\n• Target demographic: Primarily 25-45 age group\n• Success rate: Similar ventures show 35% success\n\nCase Study: Companies like [Example Co.] achieved 3x growth using similar models between 2020-2023.\n\nKey trend: Digital transformation is accelerating adoption in this space.`,
                
                conversationalAgent: `💭 Let's break this down in simple terms:\n\nSo, you're thinking about "${userInput.substring(0, 40)}..."\n\nThat's interesting! Here's what I'm wondering:\n\n1. Who exactly would use this?\n2. What makes it different from what's already out there?\n3. How would you actually make money from it?\n\nThe core idea seems solid, but I'd love to understand more about your target users. Have you thought about how you'd reach them? Also, what's your timeline looking like?`,
                
                finalConclusion: `🧠 COMPREHENSIVE ANALYSIS & RECOMMENDATION\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\nIDEA SUMMARY:\n"${userInput.substring(0, 100)}..."\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n✅ STRENGTHS:\n• Strong market potential with 15-20% annual growth\n• Addresses genuine user needs\n• Scalable business model\n• Aligns with current digital transformation trends\n\n❌ CHALLENGES:\n• Competitive market with established players\n• Requires significant initial investment\n• Customer acquisition strategy needs refinement\n• Regulatory considerations require attention\n\n📊 MARKET VIABILITY: 7/10\nBased on research, similar ventures show 35% success rate with proper execution.\n\n🎯 RECOMMENDED NEXT STEPS:\n\n1. Conduct detailed market research and competitor analysis\n2. Develop minimum viable product (MVP) for testing\n3. Identify and validate target customer segments\n4. Create financial projections for 3-5 year timeline\n5. Explore strategic partnerships to reduce entry barriers\n6. Address regulatory requirements proactively\n\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\nFINAL VERDICT:\nProceed with CAUTIOUS OPTIMISM. The idea has merit and market potential, but success will depend on thorough preparation, adequate funding, and strategic execution. Start with MVP development and validate assumptions before full-scale launch.\n\nRisk Level: MODERATE\nRecommended Action: VALIDATE & ITERATE`
            });
        }, 1500); // Simulate 1.5 second API delay
    });
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
    
    if (userInput.length < 10) {
        showNotification('Please provide more details about your idea (at least 10 characters)', 'warning');
        return;
    }
    
    // Disable button and show loading state
    analyzeBtn.disabled = true;
    analyzeBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Analyzing...';
    
    try {
        // Get agent outputs from mock backend
        const outputs = await getAgentOutputs(userInput);
        
        // Display results
        displayResults(outputs);
        
        // Scroll to results
        setTimeout(() => {
            agentOutputsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }, 300);
        
        showNotification('Analysis complete!', 'success');
        
    } catch (error) {
        console.error('Analysis failed:', error);
        showNotification('Analysis failed. Please try again.', 'error');
    } finally {
        // Reset button
        analyzeBtn.disabled = false;
        analyzeBtn.innerHTML = '<i class="fas fa-magic"></i> Analyze Idea';
    }
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
