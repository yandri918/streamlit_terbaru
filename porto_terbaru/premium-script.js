// ===================================
// PREMIUM PORTFOLIO JAVASCRIPT
// ===================================

// Loading Screen
window.addEventListener('load', () => {
    const loadingScreen = document.getElementById('loadingScreen');
    setTimeout(() => {
        loadingScreen.classList.add('hidden');
    }, 1000);
});

// Skills Radar Chart
document.addEventListener('DOMContentLoaded', () => {
    const ctx = document.getElementById('skillsRadarChart');

    if (ctx && typeof Chart !== 'undefined') {
        new Chart(ctx, {
            type: 'radar',
            data: {
                labels: [
                    'Python/Data Science',
                    'Machine Learning',
                    'Economics/Business',
                    'Web Development',
                    'Database/SQL',
                    'Cloud/DevOps',
                    'Statistics',
                    'Communication'
                ],
                datasets: [{
                    label: 'Skill Level',
                    data: [95, 90, 85, 80, 85, 75, 90, 85],
                    fill: true,
                    backgroundColor: 'rgba(139, 92, 246, 0.2)',
                    borderColor: 'rgba(139, 92, 246, 1)',
                    pointBackgroundColor: 'rgba(139, 92, 246, 1)',
                    pointBorderColor: '#fff',
                    pointHoverBackgroundColor: '#fff',
                    pointHoverBorderColor: 'rgba(139, 92, 246, 1)',
                    pointRadius: 5,
                    pointHoverRadius: 7
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                scales: {
                    r: {
                        angleLines: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        grid: {
                            color: 'rgba(255, 255, 255, 0.1)'
                        },
                        pointLabels: {
                            color: '#cbd5e1',
                            font: {
                                size: 12,
                                family: "'Inter', sans-serif"
                            }
                        },
                        ticks: {
                            color: '#94a3b8',
                            backdropColor: 'transparent',
                            stepSize: 20
                        },
                        suggestedMin: 0,
                        suggestedMax: 100
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    },
                    tooltip: {
                        backgroundColor: 'rgba(15, 23, 42, 0.9)',
                        titleColor: '#f1f5f9',
                        bodyColor: '#cbd5e1',
                        borderColor: 'rgba(139, 92, 246, 0.5)',
                        borderWidth: 1,
                        padding: 12,
                        displayColors: false,
                        callbacks: {
                            label: function (context) {
                                return context.parsed.r + '% proficiency';
                            }
                        }
                    }
                }
            }
        });
    }
});

// Enhanced Scroll Animations
const enhancedObserverOptions = {
    threshold: 0.15,
    rootMargin: '0px 0px -100px 0px'
};

const enhancedObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
            enhancedObserver.unobserve(entry.target);
        }
    });
}, enhancedObserverOptions);

document.addEventListener('DOMContentLoaded', () => {
    const animatedElements = document.querySelectorAll('.fade-in');
    animatedElements.forEach(el => {
        enhancedObserver.observe(el);
    });
});

// Timeline Horizontal Scroll Enhancement
const timelineWrapper = document.querySelector('.timeline-wrapper');
if (timelineWrapper) {
    let isDown = false;
    let startX;
    let scrollLeft;

    timelineWrapper.addEventListener('mousedown', (e) => {
        isDown = true;
        timelineWrapper.style.cursor = 'grabbing';
        startX = e.pageX - timelineWrapper.offsetLeft;
        scrollLeft = timelineWrapper.scrollLeft;
    });

    timelineWrapper.addEventListener('mouseleave', () => {
        isDown = false;
        timelineWrapper.style.cursor = 'grab';
    });

    timelineWrapper.addEventListener('mouseup', () => {
        isDown = false;
        timelineWrapper.style.cursor = 'grab';
    });

    timelineWrapper.addEventListener('mousemove', (e) => {
        if (!isDown) return;
        e.preventDefault();
        const x = e.pageX - timelineWrapper.offsetLeft;
        const walk = (x - startX) * 2;
        timelineWrapper.scrollLeft = scrollLeft - walk;
    });
}

// Case Study Details Enhancement
document.querySelectorAll('.case-study-card').forEach(card => {
    card.addEventListener('click', function (e) {
        // Add a subtle scale effect on click
        if (!e.target.closest('.case-study-link')) {
            this.style.transform = 'scale(0.98)';
            setTimeout(() => {
                this.style.transform = '';
            }, 200);
        }
    });
});

// Smooth scroll with offset for fixed navbar
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const offsetTop = target.offsetTop - 80; // Account for navbar height
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    });
});

// Add active state to navigation links
window.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');

    let current = '';
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (window.pageYOffset >= (sectionTop - 100)) {
            current = section.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
});

// Add download tracking (optional analytics)
document.querySelectorAll('a[download]').forEach(link => {
    link.addEventListener('click', function () {
        console.log('CV Downloaded:', new Date().toISOString());
        // You can add analytics tracking here
    });
});

// Performance: Preload critical resources
const preloadLinks = [
    'professional_headshot.png',
    'hero_background_1770113247484.png'
];

preloadLinks.forEach(href => {
    const link = document.createElement('link');
    link.rel = 'preload';
    link.as = 'image';
    link.href = href;
    document.head.appendChild(link);
});

console.log('%c🎨 Premium Portfolio Loaded', 'color: #8b5cf6; font-size: 18px; font-weight: bold;');
console.log('%c✨ All premium features active', 'color: #10b981; font-size: 14px;');
