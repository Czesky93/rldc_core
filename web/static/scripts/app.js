// Client-side logic for the RLdC Core web portal.
// This script handles loading current open positions from the API,
// rendering them in the table and initiating a trade cycle when the
// "Scan & Trade" button is clicked.

document.addEventListener('DOMContentLoaded', () => {
  const tradeButton = document.getElementById('tradeButton');
  const positionsTableBody = document
    .getElementById('positionsTable')
    .querySelector('tbody');
  const noPositions = document.getElementById('noPositions');

  /**
   * Fetch open positions from the API and render them in the table.
   */
  async function loadPositions() {
    try {
      const res = await fetch('/api/positions');
      const data = await res.json();
      // API returns {"positions": [...]} so handle accordingly.
      const positions = data.positions || data;
      positionsTableBody.innerHTML = '';
      if (!positions || positions.length === 0) {
        noPositions.style.display = 'block';
        return;
      }
      noPositions.style.display = 'none';
      positions.forEach((pos) => {
        const row = document.createElement('tr');
        row.innerHTML = `
          <td>${pos.symbol}</td>
          <td>${parseFloat(pos.quantity).toFixed(4)}</td>
          <td>${parseFloat(pos.entry_price).toFixed(4)}</td>
          <td>${pos.exit_price != null ? parseFloat(pos.exit_price).toFixed(4) : '-'}</td>
          <td>${pos.order_id || '-'}</td>
        `;
        positionsTableBody.appendChild(row);
      });
    } catch (err) {
      console.error('Error loading positions', err);
    }
  }

  /**
   * Trigger a trade cycle on the backend and reload positions.
   */
  async function runTrade() {
    // Disable button and update its text while the trade is executing.
    tradeButton.disabled = true;
    const originalText = tradeButton.textContent;
    tradeButton.textContent = 'Trading...';
    try {
      await fetch('/api/trade', { method: 'POST' });
      await loadPositions();
    } catch (err) {
      console.error('Error executing trade', err);
    } finally {
      tradeButton.disabled = false;
      tradeButton.textContent = originalText;
    }
  }

  // Attach event listeners and load initial data.
  tradeButton.addEventListener('click', runTrade);
  loadPositions();
});