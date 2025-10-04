async function fetchAlerts() {
  try {
    const response = await fetch('/alerts?limit=50');
    const alerts = await response.json();

    const tbody = document.querySelector('#alerts tbody');
    tbody.innerHTML = ''; // clear existing rows

    if (!alerts || alerts.length === 0) {
      const tr = document.createElement('tr');
      tr.innerHTML = `<td colspan="4" style="text-align:center;">No alerts yet</td>`;
      tbody.appendChild(tr);
      return;
    }

    for (const a of alerts) {
      const tr = document.createElement('tr');
      const t = new Date(a.timestamp);
      tr.innerHTML = `
        <td>${t.toLocaleString()}</td>
        <td class="alert-type">${a.alert_type}</td>
        <td>${a.source || ''}</td>
        <td>${a.details || ''}</td>
      `;
      tbody.appendChild(tr);
    }
  } catch (err) {
    console.error('Failed to fetch alerts:', err);
  }
}

// Initial fetch and refresh every 10 seconds
fetchAlerts();
setInterval(fetchAlerts, 10000);
