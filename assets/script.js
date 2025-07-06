// Inicializa as animações de rolagem
document.addEventListener('DOMContentLoaded', function() {
    // Inicializa o AOS (Animate On Scroll)
    AOS.init({
        duration: 800,
        easing: 'ease-out-cubic',
        once: true,
        offset: 100
    });

    // Adiciona efeito de hover nos cards de lição
    const lessonCards = document.querySelectorAll('.lesson-card');
    lessonCards.forEach(card => {
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            card.style.setProperty('--mouse-x', `${x}px`);
            card.style.setProperty('--mouse-y', `${y}px`);
        });
    });

    // Adiciona animação de clique nos botões
    const buttons = document.querySelectorAll('.btn, .action-btn');
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Efeito de ripple
            const ripple = document.createElement('span');
            ripple.className = 'ripple';
            
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = `${size}px`;
            ripple.style.left = `${x}px`;
            ripple.style.top = `${y}px`;
            
            this.appendChild(ripple);
            
            // Remove o efeito após a animação
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });

    // Adiciona tooltips
    const tooltipTriggers = document.querySelectorAll('[data-tooltip]');
    tooltipTriggers.forEach(trigger => {
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip';
        tooltip.textContent = trigger.getAttribute('data-tooltip');
        document.body.appendChild(tooltip);
        
        trigger.addEventListener('mouseenter', (e) => {
            const rect = trigger.getBoundingClientRect();
            tooltip.style.left = `${rect.left + rect.width / 2}px`;
            tooltip.style.top = `${rect.top - 10}px`;
            tooltip.style.transform = 'translate(-50%, -100%)';
            tooltip.style.opacity = '1';
        });
        
        trigger.addEventListener('mouseleave', () => {
            tooltip.style.opacity = '0';
        });
    });
});

// Função para copiar texto para a área de transferência
function copyToClipboard(text, button) {
    navigator.clipboard.writeText(text).then(() => {
        const originalHTML = button.innerHTML;
        button.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6L9 17l-5-5" /></svg><span>Copiado!</span>';
        
        setTimeout(() => {
            button.innerHTML = originalHTML;
        }, 2000);
    }).catch(err => {
        console.error('Erro ao copiar texto: ', err);
    });
}

// Adiciona efeito de parallax em elementos com data-parallax
window.addEventListener('scroll', function() {
    const parallaxElements = document.querySelectorAll('[data-parallax]');
    const scrollPosition = window.pageYOffset;
    
    parallaxElements.forEach(element => {
        const speed = parseFloat(element.getAttribute('data-parallax')) || 0.5;
        const yPos = -(scrollPosition * speed);
        element.style.transform = `translate3d(0, ${yPos}px, 0)`;
    });
});

// Adiciona efeito de máquina de escrever
function typeWriter(element, text, speed = 50) {
    let i = 0;
    element.textContent = '';
    
    function type() {
        if (i < text.length) {
            element.textContent += text.charAt(i);
            i++;
            setTimeout(type, speed);
        }
    }
    
    type();
}

// Inicializa elementos com data-typewriter
document.querySelectorAll('[data-typewriter]').forEach(element => {
    const text = element.getAttribute('data-typewriter-text') || element.textContent;
    const speed = parseInt(element.getAttribute('data-typewriter-speed')) || 50;
    typeWriter(element, text, speed);
});
