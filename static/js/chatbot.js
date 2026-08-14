document.addEventListener('DOMContentLoaded', () => {
    const chatForm = document.getElementById('chatForm');
    const chatInput = document.getElementById('chatInput');
    const chatMessagesBox = document.getElementById('chatMessagesBox');
    const quickChips = document.querySelectorAll('.quick-chip');

    // Scroll to bottom of chat
    function scrollToBottom() {
        chatMessagesBox.scrollTop = chatMessagesBox.scrollHeight;
    }
    scrollToBottom();

    // Handle Quick Chip Clicks
    quickChips.forEach(chip => {
        chip.addEventListener('click', () => {
            chatInput.value = chip.dataset.prompt;
            chatForm.dispatchEvent(new Event('submit'));
        });
    });

    // Handle Form Submit
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const message = chatInput.value.trim();
        if (!message) return;

        // Append User Message to UI immediately
        appendMessage('user', message);
        chatInput.value = '';

        // Show Bot Typing Indicator
        const typingId = showTypingIndicator();
        scrollToBottom();

        try {
            const res = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message })
            });

            const data = await res.json();
            removeTypingIndicator(typingId);

            if (data.success) {
                appendMessage('ai', data.response);
            } else {
                appendMessage('ai', 'Sorry, I encountered an issue. Please try again.');
            }
        } catch (err) {
            console.error(err);
            removeTypingIndicator(typingId);
            appendMessage('ai', 'Network error. Please check connection.');
        }

        scrollToBottom();
    });

    function appendMessage(sender, text) {
        const div = document.createElement('div');
        div.className = `chat-msg ${sender === 'user' ? 'user-msg' : 'bot-msg'}`;
        
        const avatar = sender === 'user' ? '👤' : '🤖';
        
        // Simple line break to <br> conversion for rendering formatted text
        const formatted = text.replace(/\n/g, '<br>');

        div.innerHTML = `
            <div class="msg-avatar">${avatar}</div>
            <div class="msg-bubble">${formatted}</div>
        `;

        chatMessagesBox.appendChild(div);
    }

    function showTypingIndicator() {
        const id = 'typing_' + Date.now();
        const div = document.createElement('div');
        div.id = id;
        div.className = 'chat-msg bot-msg';
        div.innerHTML = `
            <div class="msg-avatar">🤖</div>
            <div class="msg-bubble" style="color: var(--text-muted);">
                <i class="fa-solid fa-ellipsis fa-bounce"></i> CareerLanes Bot is typing...
            </div>
        `;
        chatMessagesBox.appendChild(div);
        return id;
    }

    function removeTypingIndicator(id) {
        const el = document.getElementById(id);
        if (el) el.remove();
    }
});
