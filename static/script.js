// 1. Chart.js opsætning
const ctx = document.getElementById('liveChart').getContext('2d');
const liveChart = new Chart(ctx, {
    type: 'bar',
    data: {
        labels: [], 
        datasets: [{
            label: 'Live Telemetry',
            data: [],
            borderColor: '#0066cc',
            backgroundColor: 'rgba(0, 102, 204, 0.6)',
            borderWidth: 1,
            borderRadius: 5,
            borderSkipped: 'bottom'
        }]
    },
    options: {
        responsive: true,
        animation: false, 
        scales: {
            x: { grid: { color: '#e5e5e5' }, ticks: { color: '#555' } },
            y: {
                grid: { color: '#e5e5e5' },
                ticks: { color: '#555' },
                beginAtZero: true,
                suggestedMax: 3 
            }
        },
        plugins: { legend: { display: false } }
    }
});

function getColorCode(colorName, isBackground) {
    const style = getComputedStyle(document.documentElement);
    
    switch(colorName) {
        case 'Yellow':
            return style.getPropertyValue(isBackground ? '--chart-yellow-bg' : '--chart-yellow-border').trim();
        case 'Red':
            return style.getPropertyValue(isBackground ? '--chart-red-bg' : '--chart-red-border').trim();
        case 'Blue':
        default:
            return style.getPropertyValue(isBackground ? '--chart-blue-bg' : '--chart-blue-border').trim();
    }
}

// 2. Kontrolfunktion til Flask-endpoints
async function triggerAction(endpoint) {
    try {
        await fetch(endpoint);
    } catch (error) {
        console.error("Failed to execute control action:", error);
    }
}

// 3. Event Listeners til knapperne (Erstatter onclick i HTML)
document.getElementById('btn-start').addEventListener('click', () => triggerAction('/start_via_web'));
document.getElementById('btn-stop').addEventListener('click', () => triggerAction('/stop_via_web'));
document.getElementById('btn-reset').addEventListener('click', () => triggerAction('/reset_via_web'));

// 4. Hentning og opdatering af live-data (GPIO & Grafer)
async function updateData() {
    try {
        const response = await fetch('/data');
        const data = await response.json();

        // Opdater tekst-felter
        document.getElementById('txt-time').innerText = `Time ${data.hour.toString()}`;
        document.getElementById('txt-value').innerText = `${data.value.toFixed(2)}L`;

        // Opdater Live Trigger Status (GPIO indikation)
        const program_dot = document.getElementById('trigger-dot');
        const program_txt = document.getElementById('trigger-text');

        const faring_dot = document.getElementById('status-dot');
        const faring_txt = document.getElementById('status-text');

        if (data.pulse_active) {
            program_dot.classList.add('active_program');
            program_txt.innerText = "Program Startet";
            program_txt.style.color = getColorCode("Yellow", false);
        } else {
            program_dot.classList.remove('active_program');
            program_txt.innerText = "Venter";
            program_txt.style.color = "#555566";
        }
        if (data.faring_active) {
            faring_dot.classList.add('active_faring');
            faring_txt.innerText = "Påbegyndt";
            faring_txt.style.color = getColorCode("Red", false);
        } else {
            faring_dot.classList.remove('active_faring');
            faring_txt.innerText = "Ikke Påbegyndt";
            faring_txt.style.color = "#555566";
        }

        // Opdater grafer
        let labels = data.history.map(h => `H${h.hour}`);
        let values = data.history.map(h => h.value);
        let backgroundColors = data.history.map(h => getColorCode(h.color, true));
        let borderColors = data.history.map(h => getColorCode(h.color, false));

        if (data.is_running) {
            labels.push(`H${data.hour} (Nu)`);
            values.push(data.value);
            backgroundColors.push(getColorCode(data.color, true));
            borderColors.push(getColorCode(data.color, false));
        }



        liveChart.data.labels = labels;
        liveChart.data.datasets[0].data = values;
        liveChart.data.datasets[0].backgroundColor = values;
        liveChart.data.datasets[0].backgroundColor = backgroundColors;
        liveChart.data.datasets[0].borderColor = borderColors;

        liveChart.update();

    } catch (error) {
        console.error("Error fetching live data stream:", error);
    }
}

setInterval(updateData, 100);
