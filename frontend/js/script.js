// ==========================================
// SPA - TROCA DE TELAS E ANIMAÇÕES
// ==========================================
function navigateTo(screenId) {
    const screens = document.querySelectorAll('.screen');
    screens.forEach(screen => screen.classList.remove('active'));

    const activeScreen = document.getElementById(screenId);
    if (activeScreen) {
        activeScreen.classList.add('active');
    }

    if (screenId === 'screen-trails') {
        animarBarrasDeProgresso();
        if (typeof carregarTrilhas === 'function') carregarTrilhas(); // atualiza o progresso
    }
    if (screenId === 'screen-result') gerarConfetes();
    if (screenId === 'screen-historico' && typeof carregarHistorico === 'function') {
        carregarHistorico();
    }
    if (screenId === 'screen-dashboard' && typeof carregarSequencia === 'function') {
        carregarSequencia();
    }
    if (screenId === 'screen-ranking' && typeof carregarRanking === 'function') {
        carregarRanking();
    }
    if (screenId === 'screen-erros' && typeof carregarCadernoErros === 'function') {
        carregarCadernoErros();
    }
    if (screenId === 'screen-favoritos' && typeof carregarFavoritos === 'function') {
        carregarFavoritos();
    }
}

// ==========================================
// MODO ESCURO (SWITCH)
// ==========================================
const themeSwitch = document.getElementById('theme-toggle-switch');
const savedTheme = localStorage.getItem('autotrans-theme');

if (savedTheme) {
    document.documentElement.setAttribute('data-theme', savedTheme);
    if (savedTheme === 'dark' && themeSwitch) themeSwitch.checked = true;
}

if (themeSwitch) {
    themeSwitch.addEventListener('change', function() {
        if (this.checked) {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('autotrans-theme', 'dark');
        } else {
            document.documentElement.setAttribute('data-theme', 'light');
            localStorage.setItem('autotrans-theme', 'light');
        }
    });
}

// ==========================================
// ANIMAÇÃO: BARRAS DE PROGRESSO
// ==========================================
function animarBarrasDeProgresso() {
    const barras = document.querySelectorAll('.progress-fill');
    barras.forEach(b => { b.style.width = '0%'; });
    setTimeout(() => {
        barras.forEach(b => { b.style.width = b.dataset.progresso || '0%'; });
    }, 100);
}

// ==========================================
// ANIMAÇÃO: CHUVA DE CONFETES
// ==========================================
function gerarConfetes() {
    const container = document.getElementById('screen-result');
    const colors = ['#38a169', '#ecc94b', '#e53e3e', '#3182ce', '#805ad5'];
    for (let i = 0; i < 40; i++) {
        let confete = document.createElement('div');
        confete.classList.add('confetti');
        confete.style.left = Math.random() * 100 + '%';
        confete.style.animationDuration = (Math.random() * 3 + 2) + 's';
        confete.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        container.appendChild(confete);
        setTimeout(() => confete.remove(), 5000);
    }
}

// ==========================================
// FLASHCARD 3D
// ==========================================
function virarCard(cardElement) {
    cardElement.classList.toggle('flipped');
}


// ==========================================
// NAVEGAÇÃO VIA HASH DA URL
// Ex.: /inicio#screen-profile → abre tela de perfil
// Usado pelos links da sidebar para abrir telas do SPA
// ==========================================
document.addEventListener('DOMContentLoaded', function() {
    var hash = window.location.hash.substring(1);
    if (hash) {
        var tela = document.getElementById(hash);
        if (tela && tela.classList.contains('screen')) {
            navigateTo(hash);
        }
    }
});
