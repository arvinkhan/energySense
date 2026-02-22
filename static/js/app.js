// app.js - UI wiring, sparkline generator, live-sim update
(function(){
  // if ROOMS not defined (dev fallback)
  const rooms = (typeof ROOMS !== 'undefined') ? ROOMS : [
    {name:"Conference Room", lights:"ON", fans:"OFF", waste:10, status:"warn", history:[8,9,12,10,11]},
    {name:"Server Room", lights:"OFF", fans:"ON", waste:0, status:"ok", history:[0,0,1,0,0]},
    {name:"Office 1", lights:"ON", fans:"ON", waste:35, status:"danger", history:[20,22,30,33,35]},
    {name:"Cafeteria", lights:"ON", fans:"OFF", waste:28, status:"danger", history:[18,20,25,27,28]},
  ];

  const container = document.getElementById('cardContainer');
  const totalRoomsEl = document.getElementById('totalRooms');
  const wastingEl = document.getElementById('wastingCount');
  const avgWasteEl = document.getElementById('avgWaste');
  const refreshBtn = document.getElementById('refreshBtn');

  function buildSpark(data){
    // normalize and build an SVG polyline
    const w = 120, h = 36;
    const max = Math.max(...data,1);
    const min = Math.min(...data);
    const scaleY = v => h - ((v - min) / (max - min || 1) * (h - 4)) - 2;
    const step = w / Math.max(1, data.length - 1);
    const points = data.map((v,i)=> `${i*step},${scaleY(v)}`).join(' ');
    return `<svg class="spark" viewBox="0 0 ${w} ${h}" preserveAspectRatio="none">
      <polyline points="${points}" fill="none" stroke="rgba(255,255,255,0.9)" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" />
      <polyline points="${points}" fill="rgba(74,139,232,0.06)" stroke="none" />
    </svg>`;
  }

  function statusToBadge(s){ return s === 'ok' ? 'badge ok' : s === 'warn' ? 'badge warn' : 'badge danger'; }
  function statusText(s){ return s === 'ok' ? 'Normal' : s === 'warn' ? 'Attention' : 'High Waste'; }

  function render(){
    container.innerHTML = '';
    let total = rooms.length;
    let wastingCount = rooms.filter(r=> r.status !== 'ok').length;
    let avgWaste = Math.round(rooms.reduce((a,b)=>a+b.waste,0)/Math.max(1,rooms.length));

    totalRoomsEl.textContent = total;
    wastingEl.textContent = wastingCount;
    avgWasteEl.textContent = `${avgWaste} W`;

    rooms.forEach((r, idx)=>{
      // ensure history exists
      if(!r.history || !r.history.length) r.history = Array(5).fill(r.waste || 0);

      const card = document.createElement('article');
      card.className = 'card';
      card.dataset.index = idx;

      card.innerHTML = `
        <div class="top">
          <div>
            <div class="room-title">${r.name}</div>
            <div class="room-sub">${r.location || 'Floor 1'}</div>
          </div>
          <div>
            <div class="${statusToBadge(r.status)}">${statusText(r.status)}</div>
          </div>
        </div>

        <div class="metrics">
          <div class="metric"><strong>Lights:</strong> ${r.lights}</div>
          <div class="metric"><strong>Fans:</strong> ${r.fans}</div>
          <div class="metric"><strong>Waste:</strong> ${r.waste} W</div>
          <div style="margin-left:auto">${buildSpark(r.history)}</div>
        </div>

        <div class="card-footer">
          <button class="ghost-btn details">Details</button>
          <div style="display:flex;gap:8px">
            <button class="ghost-btn toggle">Acknowledge</button>
            <button class="ghost-btn more">More</button>
          </div>
        </div>
      `;

      // click to expand
      card.querySelector('.details').addEventListener('click',()=>{
        card.classList.toggle('expanded');
        if(card.classList.contains('expanded')){
          const details = document.createElement('div');
          details.className = 'card-details';
          details.innerHTML = `<div><strong>Recent notes:</strong> ${r.note || 'No notes'}</div>
                               <div style="margin-top:10px">Trend: <em>${trendText(r.history)}</em></div>`;
          card.appendChild(details);
        } else {
          const d = card.querySelector('.card-details');
          if(d) d.remove();
        }
      });

      // acknowledge button toggles status to ok
      card.querySelector('.toggle').addEventListener('click', ()=>{
        r.status = 'ok';
        r.note = 'Acknowledged by guard';
        render();
      });

      container.appendChild(card);
    });
  }

  function trendText(hist){
    if(!hist || hist.length<2) return 'steady';
    const diff = hist[hist.length-1] - hist[0];
    return diff > 6 ? 'rising' : diff < -6 ? 'falling' : 'stable';
  }

  // Simulate live updates (replace with websocket or polling)
  function simulateUpdate(){
    rooms.forEach(r=>{
      // small random walk for demo
      const last = r.history[r.history.length-1] || (r.waste||0);
      let change = Math.round((Math.random()-0.5)*6);
      let nw = Math.max(0, last + change);
      r.history.push(nw);
      if(r.history.length>8) r.history.shift();
      // compute waste as last value
      r.waste = nw;
      // set status thresholds
      r.status = nw > 25 ? 'danger' : nw > 8 ? 'warn' : 'ok';
    });
    render();
  }

  // initial render
  render();

  // set simulated refresh every 6s
  const simInterval = setInterval(simulateUpdate, 6000);

  // manual refresh
  refreshBtn.addEventListener('click', simulateUpdate);

  // expose for debugging
  window._ENERGYSENSE = { rooms, render, simulateUpdate };

})();
