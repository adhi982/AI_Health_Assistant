document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('symptomForm');
    const submitBtn = document.getElementById('submitBtn');
    const loading = submitBtn.querySelector('.loading');
    const errorMessage = document.getElementById('errorMessage');
    const suggestions = document.getElementById('suggestions');
    const suggestionsList = document.getElementById('suggestionsList');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Reset UI
        errorMessage.style.display = 'none';
        suggestions.classList.remove('active');
        submitBtn.disabled = true;
        loading.style.display = 'block';
        
        try {
            const symptoms = document.getElementById('symptoms').value;
            const age = document.getElementById('age').value;
            const response = await fetch('/get_suggestions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ symptoms, age }),
            });
            
            const data = await response.json();
            
            if (response.ok) {
                suggestionsList.innerHTML = data.suggestions;
                suggestions.classList.add('active');
            } else {
                throw new Error(data.error || 'An error occurred');
            }
        } catch (error) {
            errorMessage.textContent = error.message;
            errorMessage.style.display = 'block';
        } finally {
            submitBtn.disabled = false;
            loading.style.display = 'none';
        }
    });

    // Feedback system
    initFeedbackSystem();
});

// Feedback system
function initFeedbackSystem() {
    const feedbackBtns = document.querySelectorAll('.feedback-btn');
    const feedbackComment = document.querySelector('.feedback-comment');
    const feedbackForm = document.querySelector('.feedback-form');
    const feedbackSuccess = document.querySelector('.feedback-success');

    feedbackBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            // Remove active class from all buttons
            feedbackBtns.forEach(b => b.classList.remove('active'));
            // Add active class to clicked button
            btn.classList.add('active');
            // Show comment box
            feedbackComment.classList.add('visible');
        });
    });

    feedbackForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const feedbackType = document.querySelector('.feedback-btn.active').dataset.type;
        const comment = document.querySelector('.feedback-comment textarea').value;

        try {
            const response = await fetch('/submit_feedback', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    type: feedbackType,
                    comment: comment,
                    suggestion_id: new Date().getTime() // Temporary ID
                })
            });

            if (response.ok) {
                feedbackForm.reset();
                feedbackComment.classList.remove('visible');
                feedbackSuccess.classList.add('visible');
                setTimeout(() => {
                    feedbackSuccess.classList.remove('visible');
                }, 3000);
            } else {
                throw new Error('Failed to submit feedback');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to submit feedback. Please try again.');
        }
    });
}
