/* =====================================================================
   Budidaya Krisan Pro — Dashboard App Logic
   FastAPI + Chart.js + Offline PWA Support
   ===================================================================== */

const API = '/api/v1';
const CACHE_KEY = 'krisan_offline_queue';

// Global State
let state = {
  batches: [],
  growthRecords: [],
  harvestRecords: [],
  aiInsights: null,
  charts: {},
  offlineQueue: [],
  currentTab: 'growth',
  filters: { variety: '', status: '', batchId: '', house: '' },
  clerkToken: null,
  clerkUser: null,
};

// =====================================================================
// INITIALIZATION
// =====================================================================
// APPLICATION LIFECYCLE & PROTECTED DASHBOARD GATE
// =====================================================================
let isDashboardStarted = false;

async function startAppWhenAuthenticated() {
  if (isDashboardStarted) return;
  isDashboardStarted = true;
  console.log('🚀 User terotentikasi. Memulai sistem dashboard Budidaya Krisan...');
  await initDashboard();
  if (window.initDigitalTwinBeds) window.initDigitalTwinBeds('House 1');
  if (window.startSensorSimulation) window.startSensorSimulation();
  if (window.runYieldSimulation) window.runYieldSimulation();
  if (window.setupCommandPalette) window.setupCommandPalette();
}

window.addEventListener('DOMContentLoaded', async () => {
  setTodayDate();
  loadOfflineQueue();
  setupEventListeners();
  setupOfflineDetection();
  registerServiceWorker();
  updateBatchHouseCalculator();
  updateStandaloneHouseCalculator();
  initSingleHouseConfig();
  if (window.initClerkAuth) window.initClerkAuth();
});

async function initDashboard() {
  try {
    await Promise.all([
      loadBatches(),
      loadSummary(),
      loadAIInsights(),
    ]);
    await Promise.all([
      loadGrowthRecords(),
      loadHarvestRecords(),
      loadChartData(),
    ]);
    populateBatchSelects();
    renderSingleHouseBatchTable();
    setApiStatus(true);
  } catch (err) {
    setApiStatus(false);
    showToast('Gagal memuat data dari server. Mode offline aktif.', 'error');
  }
}

function setTodayDate() {
  const today = new Date().toISOString().split('T')[0];
  const gDate = document.getElementById('gDate');
  const bPlantDate = document.getElementById('bPlantDate');
  const hHarvestDate = document.getElementById('hHarvestDate');
  const shPlantDate = document.getElementById('shPlantDate');
  if (gDate) gDate.value = today;
  if (bPlantDate) bPlantDate.value = today;
  if (hHarvestDate) hHarvestDate.value = today;
  if (shPlantDate && !shPlantDate.value) shPlantDate.value = today;

  // Set target harvest date = today + 112 days
  const target = new Date(Date.now() + 112 * 86400000).toISOString().split('T')[0];
  const bHarvestDate = document.getElementById('bHarvestDate');
  const shHarvestDate = document.getElementById('shHarvestDate');
  if (bHarvestDate) bHarvestDate.value = target;
  if (shHarvestDate && !shHarvestDate.value) shHarvestDate.value = target;
}

// =====================================================================
// API CALLS
// =====================================================================
async function apiFetch(path, options = {}) {
  const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) };
  if (state.clerkToken) {
    headers['Authorization'] = `Bearer ${state.clerkToken}`;
  }
  const resp = await fetch(API + path, {
    ...options,
    headers
  });
  if (!resp.ok) {
    const err = await resp.json().catch(() => ({}));
    throw new Error(err.message || `HTTP ${resp.status}`);
  }
  return resp.json();
}

async function loadBatches() {
  const params = new URLSearchParams();
  if (state.filters.status) params.set('status', state.filters.status);
  if (state.filters.variety) params.set('variety', state.filters.variety);
  const res = await apiFetch(`/batches?${params}`);
  let batches = res.data || [];
  if (state.filters.house) {
    batches = batches.filter(b => (b.house_name || 'House 1') === state.filters.house);
  }
  state.batches = batches;
  renderBatchTable(state.batches);
  document.getElementById('batchCount').textContent = `${state.batches.length} Batch`;
}

async function loadSummary() {
  const params = new URLSearchParams();
  if (state.filters.variety) params.set('variety', state.filters.variety);
  const res = await apiFetch(`/analytics/summary?${params}`);
  const d = res.data || {};
  renderKPICards(d);
}

async function loadAIInsights() {
  const params = new URLSearchParams();
  if (state.filters.variety) params.set('variety', state.filters.variety);
  const res = await apiFetch(`/analytics/ai-insights?${params}`);
  state.aiInsights = res.data || {};
  renderAIInsights(state.aiInsights);
}

async function loadGrowthRecords() {
  const params = new URLSearchParams();
  if (state.filters.batchId) params.set('batch_id', state.filters.batchId);
  if (state.filters.variety) params.set('variety', state.filters.variety);
  const res = await apiFetch(`/monitoring?${params}`);
  state.growthRecords = res.data || [];
  renderGrowthTable(state.growthRecords);
  document.getElementById('growthRecordCount').textContent = `${state.growthRecords.length} Data`;
}

async function loadHarvestRecords() {
  const res = await apiFetch('/monitoring/harvest/list');
  state.harvestRecords = res.data || [];
  renderHarvestTable(state.harvestRecords);
  document.getElementById('harvestCount').textContent = `${state.harvestRecords.length} Panen`;
}

async function loadChartData() {
  try {
    const params = new URLSearchParams();
    if (state.filters.batchId) params.set('batch_id', state.filters.batchId);

    const [growthData, financialData, gradeData] = await Promise.all([
      apiFetch(`/analytics/growth-chart?${params}`),
      apiFetch('/analytics/financial'),
      apiFetch('/analytics/grades'),
    ]);

    initGrowthChart(growthData.data || {});
    initFinancialChart(financialData.data || {});
    initGradeChart(gradeData.data || {});
    initHealthTrendChart(growthData.data || {});
  } catch (err) {
    console.error('Chart data error:', err);
  }
}

// =====================================================================
// KPI RENDERING
// =====================================================================
function renderKPICards(d) {
  setEl('kpiActiveBatches', d.total_active_batches ?? '—');
  setEl('kpiVarieties', `${d.active_varieties ?? 0} varietas aktif`);
  setEl('kpiTotalPlants', fmtNumber(d.total_plants ?? 0));
  setEl('kpiLandArea', `${d.avg_land_area_m2 ?? 0} m² lahan`);

  const hs = d.avg_health_score ?? 0;
  setEl('kpiHealthScore', hs ? hs.toFixed(1) : '—');
  const hsLabel = hs >= 80 ? '🟢 Sangat Baik' : hs >= 65 ? '🟡 Baik' : hs >= 50 ? '🟠 Cukup' : '🔴 Perlu Perhatian';
  setEl('kpiHealthSub', hsLabel);

  if (d.next_harvest_batch) {
    const nhDate = new Date(d.next_harvest_batch.target_harvest_date);
    const daysLeft = Math.ceil((nhDate - Date.now()) / 86400000);
    setEl('kpiNextHarvest', formatDate(d.next_harvest_batch.target_harvest_date));
    setEl('kpiNextHarvestBatch', `${d.next_harvest_batch.batch_code} · ${daysLeft > 0 ? daysLeft + ' hari lagi' : 'Sudah lewat'}`);
  } else {
    setEl('kpiNextHarvest', '—');
    setEl('kpiNextHarvestBatch', 'Belum ada batch aktif');
  }

  setEl('kpiEstRevenue', d.estimated_active_revenue ? 'Rp ' + fmtNumber(d.estimated_active_revenue) : '—');
  setEl('kpiTotalHarvest', `${state.harvestRecords?.length ?? 0} siklus`);
  setEl('kpiAvgRoi', `ROI rata-rata: ${d.avg_roi_pct ?? 0}%`);
}

// =====================================================================
// AI INSIGHTS RENDERING
// =====================================================================
function renderAIInsights(d) {
  if (!d) return;

  const rating = d.rating_stars ?? 3;
  const stars = '⭐'.repeat(rating) + '☆'.repeat(5 - rating);
  setEl('aiRatingStars', stars);
  setEl('aiBenchmarkStatus', d.status ?? 'Memuat...');

  const badge = document.getElementById('aiBenchmarkBadge');
  if (badge) {
    badge.style.background = rating >= 4 ? 'rgba(16,185,129,0.1)' :
                             rating >= 3 ? 'rgba(245,158,11,0.1)' : 'rgba(248,113,113,0.1)';
    badge.style.borderColor = rating >= 4 ? 'rgba(16,185,129,0.25)' :
                              rating >= 3 ? 'rgba(245,158,11,0.25)' : 'rgba(248,113,113,0.25)';
    const statusEl = document.getElementById('aiBenchmarkStatus');
    if (statusEl) statusEl.style.color = rating >= 4 ? '#a7f3d0' : rating >= 3 ? '#fde68a' : '#fca5a5';
  }

  setEl('aiStdYield', `${d.standard_yield_stems_per_m2 ?? 25} tangkai/m²`);
  const actualYieldEl = document.getElementById('aiActualYield');
  if (actualYieldEl) {
    const actual = d.actual_yield_stems_per_m2 ?? 0;
    actualYieldEl.textContent = actual > 0 ? `${actual} tangkai/m²` : '(belum ada data panen)';
    actualYieldEl.style.color = actual > (d.standard_yield_stems_per_m2 ?? 25) ? '#34d399' : '#94a3b8';
  }

  const devEl = document.getElementById('aiDeviationPct');
  if (devEl) {
    const dev = d.deviation_pct ?? 0;
    devEl.textContent = dev > 0 ? `+${dev}%` : dev < 0 ? `${dev}%` : '—';
    devEl.style.color = dev > 0 ? '#34d399' : dev < 0 ? '#f87171' : '#38bdf8';
  }

  setEl('aiHealthScore', d.avg_health_score > 0 ? `${d.avg_health_score}/100` : '—');

  const recList = document.getElementById('aiRecommendationList');
  if (recList && d.recommendations?.length) {
    recList.innerHTML = d.recommendations.map(r => `<li>${r}</li>`).join('');
  }
}

// =====================================================================
// CHARTS
// =====================================================================
const CHART_DEFAULTS = {
  responsive: true, maintainAspectRatio: false,
  plugins: {
    legend: { labels: { color: '#94a3b8', font: { family: "'Plus Jakarta Sans', sans-serif", size: 11 }, boxWidth: 12 } },
    tooltip: { backgroundColor: '#1e293b', borderColor: 'rgba(255,255,255,0.1)', borderWidth: 1, titleColor: '#f8fafc', bodyColor: '#94a3b8', cornerRadius: 8 }
  },
  scales: {
    x: { grid: { color: 'rgba(255,255,255,0.04)' }, ticks: { color: '#64748b', font: { size: 11 } } },
    y: { grid: { color: 'rgba(255,255,255,0.06)' }, ticks: { color: '#64748b', font: { size: 11 } } }
  }
};

function initGrowthChart(data) {
  const ctx = document.getElementById('growthChart');
  if (!ctx) return;
  if (state.charts.growth) state.charts.growth.destroy();

  const actualWeeks = data.actual?.weeks || [];
  const actualHeights = data.actual?.heights || [];
  const idealWeeks = data.ideal?.weeks || [];
  const idealHeights = data.ideal?.heights || [];
  const idealMin = data.ideal?.min || [];
  const idealMax = data.ideal?.max || [];

  state.charts.growth = new Chart(ctx, {
    type: 'line',
    data: {
      labels: idealWeeks.map(w => `Minggu ${w}`),
      datasets: [
        {
          label: 'Tinggi Aktual (cm)',
          data: idealWeeks.map(w => { const i = actualWeeks.indexOf(w); return i >= 0 ? actualHeights[i] : null; }),
          borderColor: '#10b981', backgroundColor: 'rgba(16,185,129,0.15)',
          pointBackgroundColor: '#10b981', pointRadius: 5, pointHoverRadius: 7,
          borderWidth: 2.5, fill: false, tension: 0.4, spanGaps: true
        },
        {
          label: 'Standar Ideal (cm)',
          data: idealHeights,
          borderColor: '#38bdf8', backgroundColor: 'transparent',
          borderDash: [6, 3], borderWidth: 2, pointRadius: 0, fill: false, tension: 0.4
        },
        {
          label: 'Zona Ideal (Maks)',
          data: idealMax,
          borderColor: 'transparent', backgroundColor: 'rgba(56,189,248,0.07)',
          fill: '+1', pointRadius: 0, tension: 0.4
        },
        {
          label: 'Zona Ideal (Min)',
          data: idealMin,
          borderColor: 'transparent', backgroundColor: 'rgba(56,189,248,0.07)',
          fill: false, pointRadius: 0, tension: 0.4
        }
      ]
    },
    options: {
      ...CHART_DEFAULTS,
      plugins: {
        ...CHART_DEFAULTS.plugins,
        tooltip: { ...CHART_DEFAULTS.plugins.tooltip,
          callbacks: { label: ctx => `${ctx.dataset.label}: ${ctx.parsed.y?.toFixed(1) ?? '—'} cm` }
        }
      },
      scales: {
        ...CHART_DEFAULTS.scales,
        y: { ...CHART_DEFAULTS.scales.y, title: { display: true, text: 'Tinggi (cm)', color: '#64748b', font: { size: 11 } } },
        x: { ...CHART_DEFAULTS.scales.x, title: { display: true, text: 'Minggu', color: '#64748b', font: { size: 11 } } }
      }
    }
  });
}

function initGradeChart(data) {
  const ctx = document.getElementById('gradeChart');
  if (!ctx) return;
  if (state.charts.grade) state.charts.grade.destroy();

  const hasData = (data.grade_a || 0) + (data.grade_b || 0) + (data.grade_c || 0) > 0;
  const gradeData = hasData ? [data.grade_a || 0, data.grade_b || 0, data.grade_c || 0] : [65, 25, 10];

  state.charts.grade = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ['Grade A (Super)', 'Grade B (Standar)', 'Grade C (Afkir)'],
      datasets: [{
        data: gradeData,
        backgroundColor: ['rgba(16,185,129,0.8)', 'rgba(56,189,248,0.8)', 'rgba(245,158,11,0.8)'],
        borderColor: ['#10b981', '#38bdf8', '#f59e0b'],
        borderWidth: 2, hoverOffset: 8
      }]
    },
    options: {
      responsive: true, maintainAspectRatio: false,
      plugins: {
        ...CHART_DEFAULTS.plugins,
        legend: { ...CHART_DEFAULTS.plugins.legend, position: 'bottom' },
        tooltip: { ...CHART_DEFAULTS.plugins.tooltip,
          callbacks: { label: ctx => ` ${ctx.label}: ${ctx.parsed} tangkai (${((ctx.parsed / ctx.dataset.data.reduce((a,b)=>a+b,0))*100).toFixed(1)}%)` }
        }
      }
    }
  });
}

function initFinancialChart(data) {
  const ctx = document.getElementById('financialChart');
  if (!ctx) return;
  if (state.charts.financial) state.charts.financial.destroy();

  const hasData = (data.labels || []).length > 0;
  const labels = hasData ? data.labels : ['Demo Data'];
  const revenue = hasData ? data.revenue : [15000000];
  const cost = hasData ? data.cost : [8000000];
  const profit = hasData ? data.profit : [7000000];

  state.charts.financial = new Chart(ctx, {
    type: 'bar',
    data: {
      labels,
      datasets: [
        { label: 'Omset Kotor', data: revenue, backgroundColor: 'rgba(16,185,129,0.6)', borderColor: '#10b981', borderWidth: 1 },
        { label: 'Biaya Produksi', data: cost, backgroundColor: 'rgba(248,113,113,0.5)', borderColor: '#f87171', borderWidth: 1 },
        { label: 'Laba Bersih', data: profit, backgroundColor: 'rgba(56,189,248,0.6)', borderColor: '#38bdf8', borderWidth: 1 }
      ]
    },
    options: {
      ...CHART_DEFAULTS,
      plugins: {
        ...CHART_DEFAULTS.plugins,
        tooltip: { ...CHART_DEFAULTS.plugins.tooltip,
          callbacks: { label: ctx => ` ${ctx.dataset.label}: Rp ${fmtNumber(ctx.parsed.y)}` }
        }
      },
      scales: { ...CHART_DEFAULTS.scales, y: { ...CHART_DEFAULTS.scales.y, ticks: { ...CHART_DEFAULTS.scales.y.ticks, callback: v => 'Rp ' + fmtCompact(v) } } }
    }
  });
}

function initHealthTrendChart(data) {
  const ctx = document.getElementById('healthTrendChart');
  if (!ctx) return;
  if (state.charts.health) state.charts.health.destroy();

  const avgScore = (state.aiInsights && state.aiInsights.summary && state.aiInsights.summary.avg_health_score) || 84.5;
  const vigorBatang = Math.min(100, Math.round(avgScore * 1.02));
  const kerapatanKanopi = Math.min(100, Math.round(avgScore * 0.96));
  const keseragaman = Math.min(100, Math.round(avgScore * 0.98));
  const ketahananPatogen = Math.min(100, Math.round(avgScore * 0.94));
  const potensiBunga = Math.min(100, Math.round(avgScore * 1.05));

  state.charts.health = new Chart(ctx, {
    type: 'radar',
    data: {
      labels: ['Vigor Batang', 'Kerapatan Kanopi', 'Keseragaman Tinggi', 'Ketahanan Patogen', 'Potensi Pembungaan'],
      datasets: [
        {
          label: 'Kondisi Aktual Batch',
          data: [vigorBatang, kerapatanKanopi, keseragaman, ketahananPatogen, potensiBunga],
          backgroundColor: 'rgba(16, 185, 129, 0.25)',
          borderColor: '#10b981',
          pointBackgroundColor: '#10b981',
          pointBorderColor: '#fff',
          pointHoverBackgroundColor: '#fff',
          pointHoverBorderColor: '#10b981',
          borderWidth: 2
        },
        {
          label: 'Standar Acuan Balithi',
          data: [80, 80, 80, 80, 80],
          backgroundColor: 'rgba(56, 189, 248, 0.08)',
          borderColor: 'rgba(56, 189, 248, 0.6)',
          borderDash: [4, 4],
          pointRadius: 0,
          borderWidth: 1.5
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        r: {
          angleLines: { color: 'rgba(255, 255, 255, 0.08)' },
          grid: { color: 'rgba(255, 255, 255, 0.08)' },
          pointLabels: { color: '#94a3b8', font: { size: 11, family: 'Plus Jakarta Sans' } },
          ticks: { backdropColor: 'transparent', color: '#64748b', stepSize: 20, min: 0, max: 100 }
        }
      },
      plugins: {
        legend: {
          display: true,
          position: 'bottom',
          labels: { color: '#94a3b8', boxWidth: 12, font: { size: 11 } }
        }
      }
    }
  });
}

// =====================================================================
// TABLE RENDERING
// =====================================================================
function renderGrowthTable(records) {
  const tbody = document.getElementById('growthTableBody');
  if (!tbody) return;
  if (!records.length) {
    tbody.innerHTML = `<tr><td colspan="11" style="text-align:center;color:var(--text-muted);padding:32px;">
      Belum ada data pertumbuhan. Klik "📈 Input Pertumbuhan" untuk memulai.
    </td></tr>`;
    return;
  }
  const search = document.getElementById('searchGrowth')?.value.toLowerCase() || '';
  const filtered = search ? records.filter(r =>
    (r.batch_code||'').toLowerCase().includes(search) ||
    (r.variety_name||'').toLowerCase().includes(search) ||
    (r.ai_grade||'').toLowerCase().includes(search)
  ) : records;

  tbody.innerHTML = filtered.map(r => {
    const dev = r.growth_deviation_pct ?? 0;
    const devColor = dev > 10 ? '#34d399' : dev < -10 ? '#f87171' : '#fbbf24';
    const devText = dev >= 0 ? `+${dev}%` : `${dev}%`;
    const anomaly = r.anomaly_detected ? `<span style="color:#f87171;font-size:11px;">⚠️ ${r.anomaly_type||'Anomali'}</span>` : `<span style="color:#34d399;font-size:11px;">✓ Normal</span>`;
    return `<tr>
      <td><strong style="color:#f8fafc;">${r.batch_code}</strong></td>
      <td><span style="font-size:12px;">${r.variety_name}</span></td>
      <td style="text-align:center;"><strong>Mgg ${r.week_number}</strong></td>
      <td>${formatDate(r.recording_date)}</td>
      <td style="text-align:center;"><strong>${r.plant_height_cm} cm</strong></td>
      <td style="text-align:center;">${r.leaf_count || '—'}</td>
      <td style="text-align:center;">
        <div style="display:flex;align-items:center;gap:6px;">
          <div style="flex:1;height:4px;background:rgba(255,255,255,0.08);border-radius:999px;overflow:hidden;">
            <div style="height:100%;width:${r.health_score||0}%;background:linear-gradient(90deg,#10b981,#2dd4bf);border-radius:999px;"></div>
          </div>
          <span style="font-size:11px;font-weight:700;color:#f8fafc;min-width:32px;">${r.health_score?.toFixed(1)||'—'}</span>
        </div>
      </td>
      <td style="text-align:center;"><span class="badge badge-${(r.ai_grade||'c').toLowerCase()}">${r.ai_grade||'—'}</span></td>
      <td style="text-align:center;color:${devColor};font-weight:600;">${devText}</td>
      <td style="text-align:center;">${anomaly}</td>
      <td>
        <button onclick="viewReport('${r.id}')" class="btn btn-secondary btn-sm" style="font-size:11px;padding:4px 8px;">📄 Laporan</button>
      </td>
    </tr>`;
  }).join('');
}

function renderBatchTable(batches) {
  const tbody = document.getElementById('batchTableBody');
  if (!tbody) return;
  if (!batches.length) {
    tbody.innerHTML = `<tr><td colspan="9" style="text-align:center;color:var(--text-muted);padding:32px;">
      Belum ada batch tanam. Klik "🌱 Batch Baru" untuk memulai.
    </td></tr>`;
    return;
  }
  const search = document.getElementById('searchBatch')?.value.toLowerCase() || '';
  const filtered = search ? batches.filter(b =>
    (b.batch_code||'').toLowerCase().includes(search) ||
    (b.variety_name||'').toLowerCase().includes(search)
  ) : batches;

  tbody.innerHTML = filtered.map(b => {
    const daysLeft = Math.ceil((new Date(b.target_harvest_date) - Date.now()) / 86400000);
    const countdown = daysLeft > 0 ? `${daysLeft}hr lagi` : daysLeft === 0 ? 'Hari ini!' : `${Math.abs(daysLeft)}hr lalu`;
    return `<tr>
      <td><strong style="color:#f8fafc;">${b.batch_code}</strong></td>
      <td>🌸 ${b.variety_name}</td>
      <td>${formatDate(b.planting_date)}</td>
      <td>${formatDate(b.target_harvest_date)} <small style="color:var(--text-muted);">(${countdown})</small></td>
      <td style="text-align:center;">${b.land_area_m2} m²</td>
      <td style="text-align:center;">${fmtNumber(b.plant_count)}</td>
      <td><span class="badge badge-${b.status}">${b.status === 'active' ? '🟢 Aktif' : b.status === 'harvested' ? '🔵 Dipanen' : '🔴 Gagal'}</span></td>
      <td style="text-align:center;color:var(--text-secondary);">${b.growth_record_count || 0} data</td>
      <td>
        <div style="display:flex;gap:6px;">
          <button onclick="loadBatchForGrowth('${b.id}')" class="btn btn-secondary btn-sm" style="font-size:11px;padding:4px 8px;" title="Input data pertumbuhan untuk batch ini">📈 Input</button>
          <button onclick="viewBatchReport('${b.id}')" class="btn btn-secondary btn-sm" style="font-size:11px;padding:4px 8px;" title="Lihat laporan batch">📄</button>
        </div>
      </td>
    </tr>`;
  }).join('');
}

function renderHarvestTable(records) {
  const tbody = document.getElementById('harvestTableBody');
  if (!tbody) return;
  if (!records.length) {
    tbody.innerHTML = `<tr><td colspan="9" style="text-align:center;color:var(--text-muted);padding:32px;">
      Belum ada data panen. Input data panen dari tab ini.
    </td></tr>`;
    return;
  }
  tbody.innerHTML = records.map(r => {
    const roiColor = r.roi_pct >= 80 ? '#34d399' : r.roi_pct >= 50 ? '#fbbf24' : '#f87171';
    return `<tr>
      <td><strong style="color:#f8fafc;">${r.batch_code}</strong></td>
      <td>${r.variety_name}</td>
      <td>${formatDate(r.harvest_date)}</td>
      <td style="text-align:center;"><strong>${fmtNumber(r.total_stems)}</strong> tangkai</td>
      <td style="text-align:center;color:#34d399;">${fmtNumber(r.grade_a_stems)}</td>
      <td>Rp ${fmtNumber(r.gross_revenue)}</td>
      <td style="color:#38bdf8;">Rp ${fmtNumber(r.net_profit)}</td>
      <td style="color:${roiColor};font-weight:700;">${r.roi_pct?.toFixed(1)}%</td>
      <td>
        <button onclick="viewHarvestReport('${r.id}')" class="btn btn-secondary btn-sm" style="font-size:11px;padding:4px 8px;">📄</button>
      </td>
    </tr>`;
  }).join('');
}

// =====================================================================
// FORM SUBMISSIONS
// =====================================================================
function setupEventListeners() {
  // Header buttons
  document.getElementById('openGrowthModalBtn')?.addEventListener('click', () => openModal('growthModal'));
  document.getElementById('openBatchModalBtn')?.addEventListener('click', () => {
    updateBatchHouseCalculator();
    openModal('batchModal');
  });
  document.getElementById('openHouseCalcModalBtn')?.addEventListener('click', () => {
    const tabBtn = document.querySelector('.section-tab[data-tab="house"]');
    if (tabBtn) {
      window.switchTab('house', tabBtn);
      document.getElementById('tabHouse')?.scrollIntoView({ behavior: 'smooth' });
    } else {
      updateStandaloneHouseCalculator();
      openModal('houseCalcModal');
    }
  });
  document.getElementById('openWebhookModalBtn')?.addEventListener('click', openWebhookModal);
  document.getElementById('closeGrowthModalBtn')?.addEventListener('click', () => closeModal('growthModal'));
  document.getElementById('openHarvestModalBtn')?.addEventListener('click', () => openModal('harvestModal'));

  // House calculator triggers
  document.getElementById('applyHouseToBatchBtn')?.addEventListener('click', applyHouseCalcToBatchModal);

  // House calculation listeners
  ['bBeds', 'bBedLength', 'bBedWidth', 'bRowsPerBed', 'bPlantSpacing'].forEach(id => {
    document.getElementById(id)?.addEventListener('input', updateBatchHouseCalculator);
  });
  ['hcBeds', 'hcLength', 'hcWidth', 'hcRows', 'hcSpacing', 'hcSurvival', 'hcStemsPerPlant', 'hcBedsPutih', 'hcBedsPink', 'hcBedsKuning'].forEach(id => {
    document.getElementById(id)?.addEventListener('input', updateStandaloneHouseCalculator);
  });

  // Filter
  document.getElementById('applyFilterBtn')?.addEventListener('click', applyFilter);
  document.getElementById('resetFilterBtn')?.addEventListener('click', resetFilter);

  // Search
  document.getElementById('searchGrowth')?.addEventListener('input', () => renderGrowthTable(state.growthRecords));
  document.getElementById('searchBatch')?.addEventListener('input', () => renderBatchTable(state.batches));

  // Forms
  document.getElementById('growthForm')?.addEventListener('submit', submitGrowthRecord);
  document.getElementById('batchForm')?.addEventListener('submit', submitBatch);
  document.getElementById('harvestForm')?.addEventListener('submit', submitHarvestRecord);
  document.getElementById('webhookConfigForm')?.addEventListener('submit', saveWebhookConfig);
  document.getElementById('testWebhookBtn')?.addEventListener('click', testWebhook);

  // Live calculator
  ['gWeek','gHeight','gLeaves','gDiameter','gBranches','gTemp','gHumidity'].forEach(id => {
    document.getElementById(id)?.addEventListener('input', updateLiveCalculator);
  });

  // Export
  document.getElementById('exportGrowthCsvBtn')?.addEventListener('click', exportGrowthCSV);
  document.getElementById('refreshDataBtn')?.addEventListener('click', () => initDashboard());

  // Sync offline
  document.getElementById('syncNowBtn')?.addEventListener('click', syncOfflineQueue);

  // Harvest modal trigger
  document.getElementById('openHarvestModalBtn')?.addEventListener('click', () => {
    populateBatchSelects();
    openModal('harvestModal');
  });
}

async function submitGrowthRecord(e) {
  e.preventDefault();
  const btn = e.target.querySelector('[type=submit]');
  btn.disabled = true;
  btn.textContent = '⏳ Menyimpan...';

  const payload = {
    batch_id: document.getElementById('gBatchId').value,
    week_number: parseInt(document.getElementById('gWeek').value),
    recording_date: document.getElementById('gDate').value,
    plant_height_cm: parseFloat(document.getElementById('gHeight').value),
    leaf_count: parseInt(document.getElementById('gLeaves').value) || null,
    stem_diameter_mm: parseFloat(document.getElementById('gDiameter').value) || null,
    branch_count: parseInt(document.getElementById('gBranches').value) || null,
    temperature_c: parseFloat(document.getElementById('gTemp').value) || null,
    humidity_pct: parseFloat(document.getElementById('gHumidity').value) || null,
    weather_condition: document.getElementById('gWeather').value,
    notes: document.getElementById('gNotes').value,
  };

  if (!payload.batch_id) {
    showToast('Pilih batch tanam terlebih dahulu.', 'error');
    btn.disabled = false;
    btn.textContent = '💾 Simpan & Analisis AI';
    return;
  }

  try {
    const res = await apiFetch('/monitoring', { method: 'POST', body: JSON.stringify(payload) });
    if (res.success) {
      showToast(`✅ Data Minggu ${payload.week_number} tersimpan! Health Score: ${res.data?.health_score?.toFixed(1) || '—'} | Grade: ${res.data?.ai_grade || '—'}`, 'success');
      closeModal('growthModal');
      e.target.reset();
      setTodayDate();
      await initDashboard();
    } else {
      showToast(res.message || 'Gagal menyimpan.', 'error');
    }
  } catch (err) {
    if (!navigator.onLine) {
      addToOfflineQueue('monitoring', payload);
      showToast('📡 Offline: Data disimpan di antrean lokal.', 'info');
      closeModal('growthModal');
    } else {
      showToast(`Error: ${err.message}`, 'error');
    }
  }
  btn.disabled = false;
  btn.textContent = '💾 Simpan & Analisis AI';
}

// =====================================================================
// HOUSE POPULATION CALCULATOR LOGIC
// =====================================================================
function updateBatchHouseCalculator() {
  const beds = Math.max(1, parseInt(document.getElementById('bBeds')?.value || '12') || 12);
  const bedLength = Math.max(1, parseFloat(document.getElementById('bBedLength')?.value || '50') || 50);
  const bedWidth = Math.max(10, parseFloat(document.getElementById('bBedWidth')?.value || '100') || 100);
  const rows = Math.max(1, parseInt(document.getElementById('bRowsPerBed')?.value || '6') || 6);
  const spacing = Math.max(1, parseFloat(document.getElementById('bPlantSpacing')?.value || '12.5') || 12.5);

  const plantsPerRow = Math.floor((bedLength * 100) / spacing);
  const plantsPerBed = plantsPerRow * rows;
  const totalPlants = plantsPerBed * beds;
  const bedAreaSingle = (bedLength * (bedWidth / 100));
  const totalBedArea = Math.round(bedAreaSingle * beds * 100) / 100;
  const density = totalBedArea > 0 ? (totalPlants / totalBedArea).toFixed(1) : 0;
  const surviving = Math.floor(totalPlants * 0.85);
  const totalStems = Math.floor(surviving * 3.5);

  const plantInput = document.getElementById('bPlantCount');
  const areaInput = document.getElementById('bArea');
  if (plantInput) plantInput.value = totalPlants;
  if (areaInput) areaInput.value = totalBedArea;

  const previewEl = document.getElementById('batchHouseCalcPreview');
  if (previewEl) {
    previewEl.innerHTML = `
      <div style="display:grid;grid-template-columns:repeat(auto-fit, minmax(130px, 1fr));gap:8px;font-size:12px;margin-top:6px;">
        <div style="background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.2);border-radius:6px;padding:6px 10px;">
          <span style="color:var(--text-muted);display:block;font-size:10px;">Per Baris</span>
          <strong style="color:var(--emerald-400);">${fmtNumber(plantsPerRow)}</strong> tanaman
        </div>
        <div style="background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.2);border-radius:6px;padding:6px 10px;">
          <span style="color:var(--text-muted);display:block;font-size:10px;">Per Bedeng</span>
          <strong style="color:var(--emerald-400);">${fmtNumber(plantsPerBed)}</strong> tanaman
        </div>
        <div style="background:rgba(16,185,129,0.15);border:1px solid rgba(16,185,129,0.3);border-radius:6px;padding:6px 10px;">
          <span style="color:var(--text-muted);display:block;font-size:10px;">Total House</span>
          <strong style="color:#34d399;font-size:14px;">${fmtNumber(totalPlants)}</strong> tanaman
        </div>
        <div style="background:rgba(59,130,246,0.08);border:1px solid rgba(59,130,246,0.2);border-radius:6px;padding:6px 10px;">
          <span style="color:var(--text-muted);display:block;font-size:10px;">Luas Bedengan</span>
          <strong style="color:#60a5fa;">${totalBedArea}</strong> m² (${density}/m²)
        </div>
        <div style="background:rgba(245,158,11,0.08);border:1px solid rgba(245,158,11,0.2);border-radius:6px;padding:6px 10px;">
          <span style="color:var(--text-muted);display:block;font-size:10px;">Estimasi Panen</span>
          <strong style="color:#fbbf24;">~${fmtNumber(totalStems)}</strong> tangkai
        </div>
      </div>
    `;
  }
}

function updateStandaloneHouseCalculator() {
  const beds = Math.max(1, parseInt(document.getElementById('hcBeds')?.value || '12') || 12);
  const bedLength = Math.max(1, parseFloat(document.getElementById('hcLength')?.value || '50') || 50);
  const bedWidth = Math.max(10, parseFloat(document.getElementById('hcWidth')?.value || '100') || 100);
  const rows = Math.max(1, parseInt(document.getElementById('hcRows')?.value || '6') || 6);
  const spacing = Math.max(1, parseFloat(document.getElementById('hcSpacing')?.value || '12.5') || 12.5);
  const survival = Math.max(0, Math.min(100, parseFloat(document.getElementById('hcSurvival')?.value || '85') || 85));
  const stemsPerPlant = Math.max(0.1, parseFloat(document.getElementById('hcStemsPerPlant')?.value || '3.5') || 3.5);

  const plantsPerRow = Math.floor((bedLength * 100) / spacing);
  const plantsPerBed = plantsPerRow * rows;
  const totalPlants = plantsPerBed * beds;
  const bedAreaSingle = (bedLength * (bedWidth / 100));
  const totalBedArea = Math.round(bedAreaSingle * beds * 100) / 100;
  const density = totalBedArea > 0 ? (totalPlants / totalBedArea).toFixed(1) : 0;
  const surviving = Math.floor(totalPlants * (survival / 100));
  const totalStems = Math.floor(surviving * stemsPerPlant);

  // Variety allocation
  const pBeds = parseInt(document.getElementById('hcBedsPutih')?.value || '0') || 0;
  const kBeds = parseInt(document.getElementById('hcBedsPink')?.value || '0') || 0;
  const yBeds = parseInt(document.getElementById('hcBedsKuning')?.value || '0') || 0;
  const allocatedBeds = pBeds + kBeds + yBeds;

  const badgeEl = document.getElementById('hcVarietyStatusBadge');
  if (badgeEl) {
    if (allocatedBeds === beds) {
      badgeEl.textContent = `✅ ${allocatedBeds} / ${beds} Bedeng (Pas)`;
      badgeEl.style.background = 'rgba(16,185,129,0.15)';
      badgeEl.style.color = '#34d399';
    } else {
      badgeEl.textContent = `⚠️ ${allocatedBeds} / ${beds} Bedeng (${allocatedBeds > beds ? 'Kelebihan' : 'Kurang'})`;
      badgeEl.style.background = 'rgba(239,68,68,0.15)';
      badgeEl.style.color = '#f87171';
    }
  }

  // Update DOM metrics
  setEl('hcResTotalPlants', fmtNumber(totalPlants));
  setEl('hcResTotalArea', totalBedArea.toFixed(1));
  setEl('hcResSurviving', fmtNumber(surviving));
  setEl('hcResTotalStems', fmtNumber(totalStems));

  setEl('hcFormulaRow', fmtNumber(plantsPerRow));
  setEl('hcFormulaBaris', rows);
  setEl('hcFormulaBed', fmtNumber(plantsPerBed));
  setEl('hcFormulaBed2', fmtNumber(plantsPerBed));
  setEl('hcFormulaBeds', beds);
  setEl('hcFormulaTotal', fmtNumber(totalPlants));
  setEl('hcFormulaDensity', density);

  // Update variety text
  setEl('hcTxtPutihBeds', pBeds);
  setEl('hcTxtPutihPlants', `${fmtNumber(pBeds * plantsPerBed)} tanaman (~${fmtNumber(Math.floor(pBeds * plantsPerBed * (survival/100) * stemsPerPlant))} tangkai)`);
  setEl('hcTxtPinkBeds', kBeds);
  setEl('hcTxtPinkPlants', `${fmtNumber(kBeds * plantsPerBed)} tanaman (~${fmtNumber(Math.floor(kBeds * plantsPerBed * (survival/100) * stemsPerPlant))} tangkai)`);
  setEl('hcTxtKuningBeds', yBeds);
  setEl('hcTxtKuningPlants', `${fmtNumber(yBeds * plantsPerBed)} tanaman (~${fmtNumber(Math.floor(yBeds * plantsPerBed * (survival/100) * stemsPerPlant))} tangkai)`);
}

function applyHouseCalcToBatchModal() {
  const houseName = document.getElementById('hcName')?.value || 'House 1';
  const beds = document.getElementById('hcBeds')?.value || '12';
  const length = document.getElementById('hcLength')?.value || '50';
  const width = document.getElementById('hcWidth')?.value || '100';
  const rows = document.getElementById('hcRows')?.value || '6';
  const spacing = document.getElementById('hcSpacing')?.value || '12.5';

  setVal('bHouseName', houseName);
  setVal('bBeds', beds);
  setVal('bBedLength', length);
  setVal('bBedWidth', width);
  setVal('bRowsPerBed', rows);
  setVal('bPlantSpacing', spacing);

  updateBatchHouseCalculator();
  closeModal('houseCalcModal');
  openModal('batchModal');
  showToast(`✅ Konfigurasi ${houseName} diterapkan ke form batch baru!`, 'success');
}

async function submitBatch(e) {
  e.preventDefault();
  const btn = e.target.querySelector('[type=submit]');
  btn.disabled = true; btn.textContent = '⏳ Membuat batch...';

  const payload = {
    variety_name: document.getElementById('bVariety').value,
    planting_date: document.getElementById('bPlantDate').value,
    target_harvest_date: document.getElementById('bHarvestDate').value,
    land_area_m2: parseFloat(document.getElementById('bArea').value),
    plant_count: parseInt(document.getElementById('bPlantCount').value),
    house_name: document.getElementById('bHouseName')?.value || 'House 1',
    beds_count: parseInt(document.getElementById('bBeds')?.value || '12'),
    bed_length_m: parseFloat(document.getElementById('bBedLength')?.value || '50'),
    rows_per_bed: parseInt(document.getElementById('bRowsPerBed')?.value || '6'),
    plant_spacing_cm: parseFloat(document.getElementById('bPlantSpacing')?.value || '12.5'),
    notes: document.getElementById('bNotes').value,
  };

  try {
    const res = await apiFetch('/batches', { method: 'POST', body: JSON.stringify(payload) });
    if (res.success) {
      showToast(`✅ Batch ${res.data.batch_code} (${res.data.house_name || 'House'}, ${fmtNumber(res.data.plant_count)} tanaman) berhasil dibuat!`, 'success');
      closeModal('batchModal');
      e.target.reset();
      setTodayDate();
      updateBatchHouseCalculator();
      await initDashboard();
    } else {
      showToast(res.message || 'Gagal membuat batch.', 'error');
    }
  } catch (err) {
    showToast(`Error: ${err.message}`, 'error');
  }
  btn.disabled = false; btn.textContent = '🌱 Buat Batch Tanam';
}

async function submitHarvestRecord(e) {
  e.preventDefault();
  const btn = e.target.querySelector('[type=submit]');
  btn.disabled = true; btn.textContent = '⏳ Menyimpan...';

  const payload = {
    batch_id: document.getElementById('hBatchId').value,
    harvest_date: document.getElementById('hHarvestDate').value,
    total_stems: parseInt(document.getElementById('hTotalStems').value),
    grade_a_stems: parseInt(document.getElementById('hGradeA').value) || 0,
    grade_b_stems: parseInt(document.getElementById('hGradeB').value) || 0,
    grade_c_stems: parseInt(document.getElementById('hGradeC').value) || 0,
    grade_a_price: parseInt(document.getElementById('hPriceA').value) || 0,
    grade_b_price: parseInt(document.getElementById('hPriceB').value) || 0,
    grade_c_price: parseInt(document.getElementById('hPriceC').value) || 0,
    production_cost: parseInt(document.getElementById('hProdCost').value) || 0,
    notes: document.getElementById('hNotes').value,
  };

  try {
    const res = await apiFetch('/monitoring/harvest', { method: 'POST', body: JSON.stringify(payload) });
    if (res.success) {
      showToast(`✅ Data panen tersimpan! ROI: ${res.data.roi_pct?.toFixed(1)}%`, 'success');
      closeModal('harvestModal');
      e.target.reset();
      await initDashboard();
    } else {
      showToast(res.message || 'Gagal menyimpan panen.', 'error');
    }
  } catch (err) {
    showToast(`Error: ${err.message}`, 'error');
  }
  btn.disabled = false; btn.textContent = '💾 Simpan Data Panen';
}

// =====================================================================
// LIVE CALCULATOR
// =====================================================================
const WEEK_STANDARDS = {
  1:{ideal:8,min:5,max:12,phase:'Adaptasi Stek'}, 2:{ideal:14,min:10,max:18,phase:'Pertumbuhan Akar'},
  3:{ideal:20,min:15,max:26,phase:'Vegetatif Awal'}, 4:{ideal:27,min:21,max:33,phase:'Vegetatif Aktif'},
  5:{ideal:34,min:27,max:41,phase:'Vegetatif Aktif'}, 6:{ideal:41,min:33,max:49,phase:'Vegetatif Akhir'},
  7:{ideal:47,min:38,max:55,phase:'Pinching'}, 8:{ideal:52,min:43,max:61,phase:'Pasca Pinching'},
  9:{ideal:56,min:46,max:65,phase:'Induksi Bunga'}, 10:{ideal:59,min:49,max:68,phase:'Kuncup Terbentuk'},
  11:{ideal:62,min:52,max:71,phase:'Kuncup Berkembang'}, 12:{ideal:65,min:55,max:74,phase:'Bunga Mekar'},
  13:{ideal:68,min:58,max:77,phase:'Bunga Mekar Penuh'}, 14:{ideal:71,min:61,max:80,phase:'Siap Panen'},
  15:{ideal:73,min:63,max:82,phase:'Panen Optimal'}, 16:{ideal:75,min:65,max:85,phase:'Panen Akhir'},
};
const WEEK_TIPS = {
  1:'Pastikan media tanam steril dan drainase baik. Hindari penyiraman berlebih di fase adaptasi.',
  2:'Cek perkembangan akar. Gunakan pupuk akar (P tinggi) untuk mendorong perakaran.',
  3:'Mulai program pupuk NPK seimbang. Jaga kelembaban 70-80% RH.',
  4:'Fase tumbuh aktif: tingkatkan N untuk mendorong vegetatif. Monitor tinggi 2x seminggu.',
  5:'Pertahankan suhu malam 15-18°C. Hindari stres air.',
  6:'Evaluasi spacing antar tanaman. Pastikan tidak terlalu rapat.',
  7:'⚡ PENTING: Lakukan pinching (pemotongan pucuk) untuk mendorong cabang produktif!',
  8:'Pasca pinching: beri pupuk P-K untuk memperkuat cabang baru.',
  9:'⚡ Mulai Short Day Treatment: tutup plastik hitam 13-14 jam/hari untuk induksi bunga.',
  10:'Kuncup mulai terbentuk. Beri pupuk K (kalium) untuk kualitas bunga.',
  11:'Monitor perkembangan kuncup. Pastikan tidak ada serangan thrips pada kuncup.',
  12:'Bunga mulai mekar. Kurangi N, fokus pada K dan Ca untuk kualitas.',
  13:'Evaluasi kematangan bunga. Target panen saat 50-60% bunga mekar.',
  14:'🌸 Siap panen! Lakukan grading dan siapkan sarana pascapanen.',
  15:'Panen optimal. Potong tangkai pagi hari untuk vase life terpanjang.',
  16:'Segera lakukan pascapanen: rendam tangkai di air + larutan preservatif.',
};

function updateLiveCalculator() {
  const week = parseInt(document.getElementById('gWeek')?.value) || 1;
  const height = parseFloat(document.getElementById('gHeight')?.value) || 0;

  const std = WEEK_STANDARDS[week] || WEEK_STANDARDS[16];
  setEl('liveStandard', `${std.ideal} cm (${std.min}–${std.max})`);
  setEl('livePhase', std.phase);

  const tip = WEEK_TIPS[week] || 'Lanjutkan monitoring rutin.';
  setEl('liveTipText', tip);

  if (!height) {
    setEl('liveDeviation', '—');
    setEl('liveHealthScore', '—');
    setEl('liveGrade', '—');
    document.getElementById('liveHealthBar').style.width = '0%';
    return;
  }

  // Deviation
  const dev = ((height - std.ideal) / std.ideal * 100).toFixed(1);
  const devEl = document.getElementById('liveDeviation');
  if (devEl) {
    devEl.textContent = (dev >= 0 ? '+' : '') + dev + '%';
    devEl.style.color = dev > 10 ? '#34d399' : dev < -15 ? '#f87171' : '#fbbf24';
  }

  // Health Score estimation
  let score = 70;
  if (std.min <= height && height <= std.max) score = 85 + Math.random() * 8;
  else if (height < std.min) score = Math.max(25, 80 - Math.abs(dev) * 1.5);
  else score = Math.max(50, 80 - Math.abs(dev));
  score = Math.min(100, Math.round(score));

  const hsEl = document.getElementById('liveHealthScore');
  if (hsEl) {
    hsEl.textContent = score + ' / 100';
    hsEl.style.color = score >= 80 ? '#34d399' : score >= 60 ? '#fbbf24' : '#f87171';
  }
  document.getElementById('liveHealthBar').style.width = score + '%';

  // Grade
  const grade = score >= 80 ? 'A' : score >= 60 ? 'B' : score >= 40 ? 'C' : 'D';
  const gradeEl = document.getElementById('liveGrade');
  if (gradeEl) {
    gradeEl.textContent = grade;
    gradeEl.style.color = grade === 'A' ? '#34d399' : grade === 'B' ? '#38bdf8' : grade === 'C' ? '#fbbf24' : '#f87171';
  }
}

// =====================================================================
// PRESETS
// =====================================================================
function loadGrowthPreset(type) {
  const today = new Date().toISOString().split('T')[0];
  const presets = {
    fiji:    { week: 8,  height: 52.5, leaves: 22, diameter: 8.5, branches: 4, temp: 18, humidity: 78 },
    reagent: { week: 10, height: 59.0, leaves: 26, diameter: 9.0, branches: 5, temp: 17, humidity: 75 },
    princess:{ week: 7,  height: 47.0, leaves: 18, diameter: 7.5, branches: 3, temp: 19, humidity: 80 },
  };
  const p = presets[type] || presets.fiji;
  setVal('gWeek', p.week);
  setVal('gHeight', p.height);
  setVal('gLeaves', p.leaves);
  setVal('gDiameter', p.diameter);
  setVal('gBranches', p.branches);
  setVal('gTemp', p.temp);
  setVal('gHumidity', p.humidity);
  setVal('gDate', today);
  updateLiveCalculator();
}

// =====================================================================
// BATCH SELECT POPULATION
// =====================================================================
// =====================================================================
function populateBatchSelects() {
  const activeBatches = state.batches.filter(b => b.status === 'active');
  const allBatches = state.batches;

  // 1. Populate filter house dropdown
  const filterHouse = document.getElementById('filterHouse');
  if (filterHouse) {
    const curHouse = filterHouse.value;
    const uniqueHouses = [...new Set(allBatches.map(b => b.house_name || 'House 1'))].filter(Boolean);
    filterHouse.innerHTML = '<option value="">Semua House</option>';
    uniqueHouses.forEach(h => {
      const opt = document.createElement('option');
      opt.value = h;
      opt.textContent = `🏠 ${h}`;
      if (h === curHouse) opt.selected = true;
      filterHouse.appendChild(opt);
    });
  }

  // 2. Populate gBatchId (Input Pertumbuhan Modal)
  ['gBatchId'].forEach(id => {
    const sel = document.getElementById(id);
    if (!sel) return;
    const current = sel.value;
    sel.innerHTML = '<option value="">-- Pilih Batch Tanam --</option>';
    activeBatches.forEach(b => {
      const opt = document.createElement('option');
      opt.value = b.id;
      opt.textContent = `${b.batch_code} — ${b.variety_name} [${b.house_name || 'House 1'}]`;
      if (b.id === current) opt.selected = true;
      sel.appendChild(opt);
    });
  });

  // 3. Populate hBatchId (Panen Modal)
  ['hBatchId'].forEach(id => {
    const sel = document.getElementById(id);
    if (!sel) return;
    sel.innerHTML = '<option value="">-- Pilih Batch Tanam --</option>';
    activeBatches.forEach(b => {
      const opt = document.createElement('option');
      opt.value = b.id;
      opt.textContent = `${b.batch_code} — ${b.variety_name} [${b.house_name || 'House 1'}]`;
      sel.appendChild(opt);
    });
  });

  // 4. Populate filter batch dropdown
  const filterBatch = document.getElementById('filterBatch');
  if (filterBatch) {
    const current = filterBatch.value;
    filterBatch.innerHTML = '<option value="">Semua Batch</option>';
    allBatches.forEach(b => {
      const opt = document.createElement('option');
      opt.value = b.id;
      opt.textContent = `${b.batch_code} — ${b.variety_name} [${b.house_name || 'House 1'}]`;
      if (b.id === current) opt.selected = true;
      filterBatch.appendChild(opt);
    });
  }

  // 5. Update Single House Batch Table
  if (typeof renderSingleHouseBatchTable === 'function') {
    renderSingleHouseBatchTable();
  }
}

function loadBatchForGrowth(batchId) {
  populateBatchSelects();
  const sel = document.getElementById('gBatchId');
  if (sel) sel.value = batchId;
  openModal('growthModal');
}

// =====================================================================
// FILTER
// =====================================================================
function applyFilter() {
  state.filters.variety = document.getElementById('filterVariety')?.value || '';
  state.filters.status = document.getElementById('filterStatus')?.value || '';
  state.filters.batchId = document.getElementById('filterBatch')?.value || '';
  state.filters.house = document.getElementById('filterHouse')?.value || '';

  const parts = [];
  if (state.filters.house) parts.push(`House: ${state.filters.house}`);
  if (state.filters.variety) parts.push(`Varietas: ${state.filters.variety}`);
  if (state.filters.status) parts.push(`Status: ${state.filters.status}`);
  if (state.filters.batchId) {
    const b = state.batches.find(x => x.id === state.filters.batchId);
    if (b) parts.push(`Batch: ${b.batch_code}`);
  }

  const summaryBar = document.getElementById('filterSummaryBar');
  const summaryText = document.getElementById('filterSummaryText');
  if (summaryBar && summaryText) {
    if (parts.length) {
      summaryBar.style.display = 'flex';
      summaryText.textContent = 'Filter aktif: ' + parts.join(' · ');
    } else {
      summaryBar.style.display = 'none';
    }
  }
  initDashboard();
}

function resetFilter() {
  state.filters = { variety: '', status: '', batchId: '', house: '' };
  setVal('filterVariety', '');
  setVal('filterStatus', '');
  setVal('filterBatch', '');
  setVal('filterHouse', '');
  const summaryBar = document.getElementById('filterSummaryBar');
  if (summaryBar) summaryBar.style.display = 'none';
  initDashboard();
}

// =====================================================================
// MODAL HELPERS
// =====================================================================
function openModal(id) {
  const m = document.getElementById(id);
  if (m) m.classList.add('active');
}
function closeModal(id) {
  const m = document.getElementById(id);
  if (m) m.classList.remove('active');
}
// Close on backdrop click
document.addEventListener('click', e => {
  if (e.target.classList.contains('modal-overlay')) {
    e.target.classList.remove('active');
  }
});

// =====================================================================
// WEBHOOK CONFIG
// =====================================================================
async function openWebhookModal() {
  try {
    const res = await apiFetch('/config/webhook');
    const cfg = res.data || {};
    setVal('webhookUrlInput', cfg.webhook_url || '');
    document.getElementById('webhookEnabledToggle').checked = !!cfg.is_enabled;
  } catch(e) {}
  openModal('webhookModal');
}

async function saveWebhookConfig(e) {
  e.preventDefault();
  const payload = {
    webhook_url: document.getElementById('webhookUrlInput').value,
    is_enabled: document.getElementById('webhookEnabledToggle').checked,
  };
  try {
    await apiFetch('/config/webhook', { method: 'POST', body: JSON.stringify(payload) });
    showToast('✅ Konfigurasi webhook berhasil disimpan.', 'success');
    closeModal('webhookModal');
  } catch(e) { showToast('Gagal menyimpan konfigurasi.', 'error'); }
}

async function testWebhook() {
  showToast('🔄 Mengirim pesan uji coba...', 'info');
  try {
    const res = await apiFetch('/config/webhook/test', { method: 'POST' });
    showToast(res.success ? '✅ Pesan uji coba berhasil dikirim!' : '❌ ' + res.message, res.success ? 'success' : 'error');
  } catch(e) { showToast('Gagal mengirim uji coba.', 'error'); }
}

// =====================================================================
// REPORT NAVIGATION
// =====================================================================
function viewReport(recordId) {
  window.open(`${API}/monitoring/${recordId}/report`, '_blank');
}
function viewBatchReport(batchId) {
  window.open(`${API}/monitoring/batch/${batchId}/report`, '_blank');
}
function viewHarvestReport(recordId) {
  showToast('Fitur laporan panen segera hadir.', 'info');
}

// =====================================================================
// CSV EXPORT
// =====================================================================
async function exportGrowthCSV() {
  const params = state.filters.batchId ? `?batch_id=${state.filters.batchId}` : '';
  window.location.href = `${API}/monitoring/export/csv${params}`;
}

// =====================================================================
// TAB SWITCHING
// =====================================================================
function switchTab(tab, btn) {
  state.currentTab = tab;
  document.querySelectorAll('.section-tab').forEach(t => t.classList.remove('active'));
  btn.classList.add('active');
  ['growth','batches','harvests'].forEach(t => {
    const el = document.getElementById(`tab${t.charAt(0).toUpperCase() + t.slice(1)}`);
    if (el) el.style.display = t === tab ? 'block' : 'none';
  });
}

// =====================================================================
// TOAST NOTIFICATIONS
// =====================================================================
function showToast(message, type = 'info', duration = 5000) {
  const container = document.getElementById('toastContainer');
  if (!container) return;

  const icons = { success: '✅', error: '❌', info: 'ℹ️', warning: '⚠️' };
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `<span style="font-size:16px;">${icons[type] || 'ℹ️'}</span><span>${message}</span>`;
  container.appendChild(toast);

  setTimeout(() => {
    toast.style.animation = 'slideInRight 0.3s ease reverse';
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

// =====================================================================
// OFFLINE PWA
// =====================================================================
function setupOfflineDetection() {
  const updateStatus = () => {
    const banner = document.getElementById('offlineSyncBanner');
    if (!navigator.onLine && banner) {
      banner.style.display = 'flex';
      showToast('📡 Koneksi internet terputus. Mode offline aktif.', 'warning');
    } else if (navigator.onLine && banner) {
      banner.style.display = 'none';
      if (state.offlineQueue.length > 0) syncOfflineQueue();
    }
    setApiStatus(navigator.onLine);
  };
  window.addEventListener('online', updateStatus);
  window.addEventListener('offline', updateStatus);
}

function addToOfflineQueue(endpoint, payload) {
  state.offlineQueue.push({ endpoint, payload, timestamp: Date.now() });
  localStorage.setItem(CACHE_KEY, JSON.stringify(state.offlineQueue));
  document.getElementById('offlineQueueCount').textContent = state.offlineQueue.length;
}

function loadOfflineQueue() {
  try {
    const saved = localStorage.getItem(CACHE_KEY);
    if (saved) state.offlineQueue = JSON.parse(saved);
    document.getElementById('offlineQueueCount').textContent = state.offlineQueue.length;
  } catch(e) {}
}

async function syncOfflineQueue() {
  if (!state.offlineQueue.length) return;
  showToast(`🔄 Menyinkronisasi ${state.offlineQueue.length} data offline...`, 'info');
  let synced = 0;
  const remaining = [];
  for (const item of state.offlineQueue) {
    try {
      await apiFetch('/' + item.endpoint, { method: 'POST', body: JSON.stringify(item.payload) });
      synced++;
    } catch(e) { remaining.push(item); }
  }
  state.offlineQueue = remaining;
  localStorage.setItem(CACHE_KEY, JSON.stringify(remaining));
  document.getElementById('offlineQueueCount').textContent = remaining.length;
  if (synced > 0) {
    showToast(`✅ ${synced} data offline berhasil disinkronisasi.`, 'success');
    await initDashboard();
  }
}

async function registerServiceWorker() {
  if ('serviceWorker' in navigator) {
    try { await navigator.serviceWorker.register('/sw.js'); } catch(e) {}
  }
}

// =====================================================================
// API STATUS
// =====================================================================
function setApiStatus(online) {
  const dot = document.getElementById('networkPulseDot');
  const text = document.getElementById('apiStatusText');
  if (dot && text) {
    dot.style.background = online ? '#34d399' : '#f87171';
    dot.style.boxShadow = `0 0 6px ${online ? '#34d399' : '#f87171'}`;
    text.textContent = online ? 'Online & Siap' : 'Offline';
    text.style.color = online ? '#a7f3d0' : '#fca5a5';
  }
}

// =====================================================================
// UTILITIES
// =====================================================================
function setEl(id, text) {
  const el = document.getElementById(id);
  if (el) el.textContent = text;
}
function setVal(id, val) {
  const el = document.getElementById(id);
  if (el) el.value = val;
}
function fmtNumber(n) {
  return (n || 0).toLocaleString('id-ID');
}
function fmtCompact(n) {
  if (n >= 1e9) return (n/1e9).toFixed(1) + 'M';
  if (n >= 1e6) return (n/1e6).toFixed(1) + 'jt';
  if (n >= 1e3) return (n/1e3).toFixed(0) + 'rb';
  return n;
}
function formatDate(dateStr) {
  if (!dateStr) return '—';
  try {
    return new Date(dateStr).toLocaleDateString('id-ID', { day:'2-digit', month:'short', year:'numeric' });
  } catch(e) { return dateStr; }
}

// =====================================================================
// TAB SWITCHING & SINGLE HOUSE BATCH CONTROLLER
// =====================================================================
window.switchTab = function(tabId, el) {
  document.querySelectorAll('.section-tab').forEach(btn => btn.classList.remove('active'));
  if (el) el.classList.add('active');

  const tabIds = ['tabGrowth', 'tabBatches', 'tabHarvests', 'tabHouse'];
  tabIds.forEach(id => {
    const sec = document.getElementById(id);
    if (sec) sec.style.display = 'none';
  });

  const targetMap = {
    'growth': 'tabGrowth',
    'batches': 'tabBatches',
    'harvests': 'tabHarvests',
    'house': 'tabHouse',
  };
  const targetSec = document.getElementById(targetMap[tabId]);
  if (targetSec) {
    targetSec.style.display = 'block';
    if (tabId === 'house') {
      updateSingleHouseCalc();
      renderSingleHouseBatchTable();
    }
  }
};

// =====================================================================
// SINGLE HOUSE CONFIGURATION & BATCH INPUT CONTROLLER
// =====================================================================

window.initSingleHouseConfig = function() {
  const today = new Date().toISOString().split('T')[0];
  const target = new Date(Date.now() + 112 * 86400000).toISOString().split('T')[0];

  const pDate = document.getElementById('shPlantDate');
  const hDate = document.getElementById('shHarvestDate');
  if (pDate && !pDate.value) pDate.value = today;
  if (hDate && !hDate.value) hDate.value = target;

  updateSingleHouseCalc();
  renderSingleHouseBatchTable();
};

window.onSingleHouseSelectChange = function(val) {
  const nameInput = document.getElementById('shHouseName');
  if (!nameInput) return;
  if (val === 'custom') {
    nameInput.value = '';
    nameInput.focus();
  } else {
    nameInput.value = val;
  }
  updateSingleHouseCalc();
};

window.onSingleHouseVarietySelectChange = function(val) {
  const input = document.getElementById('shVariety');
  if (!input) return;
  if (val === 'custom') {
    input.value = '';
    input.focus();
    input.placeholder = 'Ketik nama varietas krisan baru...';
  } else {
    input.value = val;
  }
  updateSingleHouseCalc();
};

window.onBatchVarietySelectChange = function(val) {
  const input = document.getElementById('bVariety');
  if (!input) return;
  if (val === 'custom') {
    input.value = '';
    input.focus();
    input.placeholder = 'Ketik nama varietas krisan baru...';
  } else {
    input.value = val;
  }
};

window.onSingleHousePlantDateChange = function(val) {
  if (!val) return;
  try {
    const pDate = new Date(val);
    const hDate = new Date(pDate.getTime() + 112 * 86400000);
    const targetInput = document.getElementById('shHarvestDate');
    if (targetInput) targetInput.value = hDate.toISOString().split('T')[0];
  } catch (e) {
    console.error('Date calc error:', e);
  }
};

window.onSingleHouseColorChange = function() {
  const beds = parseInt(document.getElementById('shBeds')?.value) || 12;
  const pBeds = parseInt(document.getElementById('shBedsPutih')?.value) || 0;
  const kBeds = parseInt(document.getElementById('shBedsPink')?.value) || 0;
  const yBeds = parseInt(document.getElementById('shBedsKuning')?.value) || 0;
  const sum = pBeds + kBeds + yBeds;

  const badge = document.getElementById('shAllocBadge');
  if (badge) {
    if (sum === beds) {
      badge.textContent = `${sum} / ${beds} Bedeng (Pas ✓)`;
      badge.style.color = '#34d399';
    } else if (sum < beds) {
      badge.textContent = `${sum} / ${beds} Bedeng (Kurang ${beds - sum})`;
      badge.style.color = '#f59e0b';
    } else {
      badge.textContent = `${sum} / ${beds} Bedeng (Lebih ${sum - beds} ⚠️)`;
      badge.style.color = '#f87171';
    }
  }

  updateSingleHouseCalc();
};

window.updateSingleHouseCalc = function() {
  const houseName = document.getElementById('shHouseName')?.value?.trim() || 'House 1';
  const beds = Math.max(1, parseInt(document.getElementById('shBeds')?.value) || 12);
  const length = Math.max(1, parseFloat(document.getElementById('shBedLength')?.value) || 50);
  const width = Math.max(10, parseFloat(document.getElementById('shBedWidth')?.value) || 100);
  const rows = Math.max(1, parseInt(document.getElementById('shRows')?.value) || 6);
  const spacing = Math.max(1, parseFloat(document.getElementById('shSpacing')?.value) || 12.5);
  const survival = Math.max(0, Math.min(100, parseFloat(document.getElementById('shSurvival')?.value) || 85));
  const stemsPerPlant = 3.5;

  const plantsPerRow = Math.floor((length * 100) / spacing);
  const plantsPerBed = plantsPerRow * rows;
  const totalPlants = plantsPerBed * beds;
  const bedAreaSingle = length * (width / 100);
  const totalBedArea = Math.round(bedAreaSingle * beds * 10) / 10;
  const density = totalBedArea > 0 ? (totalPlants / totalBedArea).toFixed(1) : '0';
  const surviving = Math.floor(totalPlants * (survival / 100));
  const totalStems = Math.floor(surviving * stemsPerPlant);

  // Variety breakdown
  const pBeds = parseInt(document.getElementById('shBedsPutih')?.value) || 0;
  const kBeds = parseInt(document.getElementById('shBedsPink')?.value) || 0;
  const yBeds = parseInt(document.getElementById('shBedsKuning')?.value) || 0;

  const pPlants = pBeds * plantsPerBed;
  const pStems = Math.floor(pPlants * (survival / 100) * stemsPerPlant);
  const kPlants = kBeds * plantsPerBed;
  const kStems = Math.floor(kPlants * (survival / 100) * stemsPerPlant);
  const yPlants = yBeds * plantsPerBed;
  const yStems = Math.floor(yPlants * (survival / 100) * stemsPerPlant);

  // Update DOM metrics
  setEl('shLiveBadgeHouse', houseName);
  setEl('shLiveTotalPlants', fmtNumber(totalPlants));
  setEl('shLivePlantsPerRow', fmtNumber(plantsPerRow));
  setEl('shLivePlantsPerBed', fmtNumber(plantsPerBed));
  setEl('shLiveTotalArea', `${totalBedArea.toFixed(1)} m²`);
  setEl('shLiveDensity', `${density} tan/m²`);
  setEl('shLiveTotalStems', `~${fmtNumber(totalStems)}`);

  setEl('shLivePlantsWhite', `${fmtNumber(pPlants)} btg`);
  setEl('shLiveStemsWhite', `~${fmtNumber(pStems)} tgk`);
  setEl('shLivePlantsPink', `${fmtNumber(kPlants)} btg`);
  setEl('shLiveStemsPink', `~${fmtNumber(kStems)} tgk`);
  setEl('shLivePlantsYellow', `${fmtNumber(yPlants)} btg`);
  setEl('shLiveStemsYellow', `~${fmtNumber(yStems)} tgk`);

  return {
    houseName,
    beds,
    length,
    width,
    rows,
    spacing,
    survival,
    plantsPerRow,
    plantsPerBed,
    totalPlants,
    totalBedArea,
    density,
    totalStems,
  };
};

window.resetSingleHouseConfig = function() {
  setVal('shHouseSelect', 'House 1');
  setVal('shHouseName', 'House 1');
  setVal('shVarietySelect', 'Fiji White');
  setVal('shVariety', 'Fiji White');
  setVal('shBeds', 12);
  setVal('shBedLength', 50);
  setVal('shBedWidth', 100);
  setVal('shRows', '6');
  setVal('shSpacing', '12.5');
  setVal('shSurvival', 85);
  setVal('shBedsPutih', 4);
  setVal('shBedsPink', 4);
  setVal('shBedsKuning', 4);
  setVal('shNotes', '');

  const today = new Date().toISOString().split('T')[0];
  const target = new Date(Date.now() + 112 * 86400000).toISOString().split('T')[0];
  setVal('shPlantDate', today);
  setVal('shHarvestDate', target);

  window.onSingleHouseColorChange();
  showToast('🔄 Konfigurasi House berhasil di-reset ke nilai standar.', 'info');
};

window.submitSingleHouseBatch = async function() {
  const btn = document.getElementById('btnSubmitSingleHouseBatch');
  if (btn) {
    btn.disabled = true;
    btn.textContent = '⏳ Menyimpan ke Database...';
  }

  try {
    const calc = window.updateSingleHouseCalc();
    const houseName = document.getElementById('shHouseName')?.value?.trim() || 'House 1';
    const variety = document.getElementById('shVariety')?.value || 'Fiji White';
    const plantDate = document.getElementById('shPlantDate')?.value;
    const harvestDate = document.getElementById('shHarvestDate')?.value;
    const notes = document.getElementById('shNotes')?.value?.trim() || '';

    if (!plantDate) {
      showToast('⚠️ Silakan tentukan Tanggal Tanam terlebih dahulu.', 'error');
      if (btn) { btn.disabled = false; btn.textContent = '🌱 Simpan & Buat Batch Baru ke Database'; }
      return;
    }

    const payload = {
      variety_name: variety,
      planting_date: plantDate,
      target_harvest_date: harvestDate || null,
      land_area_m2: calc.totalBedArea,
      plant_count: calc.totalPlants,
      house_name: houseName,
      beds: calc.beds,
      bed_length_m: calc.length,
      bed_width_cm: calc.width,
      rows_per_bed: calc.rows,
      plant_spacing_cm: calc.spacing,
      notes: notes || `Batch dari konfigurasi ${houseName} (${calc.beds} bedeng × ${calc.length}m, ${calc.rows} baris)`,
    };

    const res = await apiFetch('/batches', {
      method: 'POST',
      body: JSON.stringify(payload)
    });

    if (res.success) {
      showToast(`🎉 Berhasil! Batch ${res.data.batch_code} (${houseName}) tersimpan dan siap dimonitor!`, 'success');
      await initDashboard();

      // Suggest next house number in dropdown
      const nextMatch = houseName.match(/House\s*(\d+)/i);
      if (nextMatch) {
        const nextNum = parseInt(nextMatch[1]) + 1;
        const nextName = `House ${nextNum}`;
        const select = document.getElementById('shHouseSelect');
        if (select) {
          const opt = Array.from(select.options).find(o => o.value === nextName);
          if (opt) {
            select.value = nextName;
            setVal('shHouseName', nextName);
          } else {
            setVal('shHouseName', nextName);
          }
          updateSingleHouseCalc();
        }
      }
    } else {
      showToast(res.message || 'Gagal menyimpan batch ke database.', 'error');
    }
  } catch (err) {
    showToast(`Error: ${err.message}`, 'error');
  } finally {
    if (btn) {
      btn.disabled = false;
      btn.textContent = '🌱 Simpan & Buat Batch Baru ke Database';
    }
  }
};

window.renderSingleHouseBatchTable = function() {
  const tbody = document.getElementById('singleHouseBatchTableBody');
  const countBadge = document.getElementById('dashHouseBatchCountBadge');
  if (!tbody) return;

  const batches = state.batches || [];
  if (countBadge) {
    countBadge.textContent = `${batches.length} Batch Terdaftar`;
  }

  if (batches.length === 0) {
    tbody.innerHTML = `<tr><td colspan="9" style="text-align:center;color:var(--text-muted);padding:24px;">Belum ada batch tersimpan. Gunakan form di atas untuk membuat batch baru.</td></tr>`;
    return;
  }

  tbody.innerHTML = batches.map(b => {
    const statusBadge = b.status === 'active'
      ? `<span class="badge badge-active">🟢 Aktif</span>`
      : `<span class="badge badge-harvested">🟣 Selesai</span>`;
    const houseLabel = b.house_name || 'House 1';

    return `
      <tr>
        <td><strong style="color:#f8fafc;">${b.batch_code}</strong></td>
        <td>
          <span style="font-weight:600;color:var(--emerald-400);background:rgba(16,185,129,0.1);padding:2px 8px;border-radius:4px;font-size:11px;">
            🏠 ${houseLabel}
          </span>
        </td>
        <td>${b.variety_name}</td>
        <td>${formatDate(b.planting_date)}</td>
        <td>${formatDate(b.target_harvest_date)}</td>
        <td style="font-weight:700;color:#34d399;">${fmtNumber(b.plant_count)} tan</td>
        <td style="color:#60a5fa;">${b.land_area_m2} m²</td>
        <td>${statusBadge}</td>
        <td>
          <button type="button" class="btn btn-secondary btn-sm" onclick="openGrowthForBatch('${b.id}')" style="font-size:11px;padding:3px 8px;color:var(--emerald-400);border-color:rgba(16,185,129,0.3);">
            📈 Monitoring
          </button>
        </td>
      </tr>
    `;
  }).join('');
};

window.openGrowthForBatch = function(batchId) {
  const sel = document.getElementById('gBatchId');
  if (sel) {
    sel.value = batchId;
  }
  updateLiveCalculator();
  openModal('growthModal');
};

// Compatibility aliases
window.useHouseForBatch = function(index) {
  const name = `House ${index + 1}`;
  setVal('shHouseSelect', name);
  setVal('shHouseName', name);
  updateSingleHouseCalc();
  document.getElementById('tabHouse')?.scrollIntoView({ behavior: 'smooth' });
};

// =====================================================================
// DIGITAL TWIN: 12-BED GREENHOUSE MATRIX VISUALIZER
// =====================================================================
let currentDtHouse = 'House 1';
let selectedDtBed = 1;

window.initDigitalTwinBeds = function(houseName = 'House 1') {
  currentDtHouse = houseName;
  const container = document.getElementById('dtBedGrid');
  if (!container) return;

  // Bed configuration: 12 beds
  // Beds 1-4: White (Fiji White / Reagent White)
  // Beds 5-8: Pink (Reagent Pink / Princess Pink)
  // Beds 9-12: Yellow (Fiji Yellow / Gold Princess)
  const bedsData = [];
  for (let i = 1; i <= 12; i++) {
    let colorType = 'white';
    let variety = 'Fiji White';
    let tagClass = 'dt-tag-white';
    let fillClass = 'dt-fill-white';
    let vigor = 85 + (i * 3 % 12);

    if (i >= 5 && i <= 8) {
      colorType = 'pink';
      variety = 'Reagent Pink';
      tagClass = 'dt-tag-pink';
      fillClass = 'dt-fill-pink';
      vigor = 82 + (i * 2 % 10);
    } else if (i >= 9) {
      colorType = 'yellow';
      variety = 'Fiji Yellow';
      tagClass = 'dt-tag-yellow';
      fillClass = 'dt-fill-yellow';
      vigor = 88 + (i * 4 % 8);
    }

    // Days After Planting (HST)
    const dap = 42 + (i * 2);
    bedsData.push({
      bedNum: i,
      variety,
      colorType,
      tagClass,
      fillClass,
      plants: 2400,
      dap,
      vigor,
      health: vigor >= 85 ? '🟢 Prima' : '🟡 Baik'
    });
  }

  container.innerHTML = bedsData.map(b => `
    <div class="dt-bed-card ${b.bedNum === selectedDtBed ? 'selected' : ''}" onclick="inspectBed(${b.bedNum}, '${b.variety}', ${b.plants}, ${b.dap}, ${b.vigor})">
      <div class="dt-bed-top">
        <strong style="font-size:12px;color:#fff;">Bed ${b.bedNum}</strong>
        <span class="dt-bed-tag ${b.tagClass}">${b.variety.split(' ')[0]}</span>
      </div>
      <div style="font-size:11px;color:var(--text-secondary);display:flex;justify-content:space-between;margin-bottom:2px;">
        <span>Populasi:</span>
        <strong style="color:#fff;" class="mono">${b.plants.toLocaleString()}</strong>
      </div>
      <div style="font-size:11px;color:var(--text-secondary);display:flex;justify-content:space-between;">
        <span>Umur:</span>
        <span style="color:var(--cyan-400);">${b.dap} HST</span>
      </div>
      <div class="dt-bed-bar">
        <div class="dt-bed-fill ${b.fillClass}" style="width:${b.vigor}%;"></div>
      </div>
      <div style="display:flex;justify-content:space-between;align-items:center;font-size:10px;margin-top:4px;">
        <span style="color:var(--text-muted);">Vigor: ${b.vigor}%</span>
        <span>${b.health}</span>
      </div>
    </div>
  `).join('');
};

window.switchDtHouse = function(houseName, btn) {
  document.querySelectorAll('.dt-house-btn').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');
  window.initDigitalTwinBeds(houseName);
  showToast(`🏛️ Digital Twin beralih ke ${houseName}`, 'info');
};

window.inspectBed = function(bedNum, variety, plants, dap, vigor) {
  selectedDtBed = bedNum;
  document.querySelectorAll('.dt-bed-card').forEach((el, idx) => {
    if (idx + 1 === bedNum) el.classList.add('selected');
    else el.classList.remove('selected');
  });

  const infoEl = document.getElementById('dtSelectedBedInfo');
  if (infoEl) {
    infoEl.innerHTML = `
      🌿 <strong>Bedeng ${bedNum} (${variety}):</strong> 2,400 bibit • 50m × 1m (6 baris @12.5cm) • Umur <strong>${dap} HST</strong> • Vigor Score <strong>${vigor}/100</strong> • Est. Panen: <strong>~7,140 tangkai</strong>
    `;
  }
};

// =====================================================================
// SENSOR TICKER & REAL-TIME VPD CALCULATION
// =====================================================================
window.startSensorSimulation = function() {
  const tempEl = document.getElementById('liveSensorTemp');
  const humEl = document.getElementById('liveSensorHumidity');
  const vpdEl = document.getElementById('liveSensorVpd');
  const luxEl = document.getElementById('liveSensorLux');
  const clockEl = document.getElementById('liveClockDisplay');

  function updateSensors() {
    const now = new Date();
    if (clockEl) {
      clockEl.textContent = now.toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit', second: '2-digit' }) + ' WIB';
    }

    // Microclimate subtle natural fluctuation
    const baseTemp = 21.2 + Math.sin(now.getTime() / 60000) * 0.8;
    const baseHum = 76.0 + Math.cos(now.getTime() / 80000) * 3.0;
    const lux = Math.round(34000 + Math.sin(now.getTime() / 45000) * 1500);

    // Vapor Pressure Deficit calculation:
    // SVP = 0.61078 * exp((17.27 * T) / (T + 237.3))
    // AVP = SVP * (RH / 100)
    // VPD = SVP - AVP = SVP * (1 - RH / 100)
    const svp = 0.61078 * Math.exp((17.27 * baseTemp) / (baseTemp + 237.3));
    const vpd = svp * (1 - baseHum / 100);

    if (tempEl) tempEl.textContent = `${baseTemp.toFixed(1)}°C`;
    if (humEl) humEl.textContent = `${baseHum.toFixed(0)}%`;
    if (vpdEl) vpdEl.textContent = `${vpd.toFixed(2)} kPa`;
    if (luxEl) luxEl.textContent = `${lux.toLocaleString()} lx`;
  }

  updateSensors();
  setInterval(updateSensors, 2000);
};

// =====================================================================
// INTERACTIVE AI YIELD & PROFIT SIMULATOR
// =====================================================================
window.runYieldSimulation = function() {
  const survival = parseFloat(document.getElementById('simSurvivalSlider')?.value || 85);
  const stemsPerPlant = parseFloat(document.getElementById('simStemsSlider')?.value || 3.5);
  const avgPrice = parseFloat(document.getElementById('simPriceSlider')?.value || 22000);

  // Update slider labels
  const survValEl = document.getElementById('simSurvivalVal');
  const stemsValEl = document.getElementById('simStemsVal');
  const priceValEl = document.getElementById('simPriceVal');
  if (survValEl) survValEl.textContent = `${survival}%`;
  if (stemsValEl) stemsValEl.textContent = `${stemsPerPlant.toFixed(1)}`;
  if (priceValEl) priceValEl.textContent = `Rp ${avgPrice.toLocaleString()}`;

  // Standard greenhouse population: 28,800 plants
  const basePlants = 28800;
  const survivingPlants = basePlants * (survival / 100);
  const totalStems = Math.round(survivingPlants * stemsPerPlant);
  const grossRevenue = totalStems * avgPrice;

  // Operational cost benchmark (bibit, media tanam, nutrisi, tenaga kerja, listrik black-out)
  const estCost = Math.round(basePlants * 22200);
  const netProfit = grossRevenue - estCost;
  const roi = ((netProfit / estCost) * 100).toFixed(1);

  // Update result elements
  const resStems = document.getElementById('simResultStems');
  const resRev = document.getElementById('simResultRevenue');
  const resCost = document.getElementById('simResultCost');
  const resProfit = document.getElementById('simResultProfit');
  const resRoi = document.getElementById('simResultRoi');

  if (resStems) resStems.textContent = `${totalStems.toLocaleString()} tgk`;
  if (resRev) resRev.textContent = `Rp ${grossRevenue.toLocaleString()}`;
  if (resCost) resCost.textContent = `Rp ${estCost.toLocaleString()}`;
  if (resProfit) resProfit.textContent = `Rp ${netProfit.toLocaleString()}`;
  if (resRoi) resRoi.textContent = `${roi}%`;
};

// =====================================================================
// CHART PERIOD FILTER
// =====================================================================
window.filterChartPeriod = function(period) {
  if (!state.charts.growth) return;
  const chart = state.charts.growth;

  if (period === 'veg') {
    chart.options.scales.x.min = 'Minggu 1';
    chart.options.scales.x.max = 'Minggu 6';
    showToast('📈 Menampilkan Fase Vegetatif (Minggu 1 - 6)', 'info');
  } else if (period === 'gen') {
    chart.options.scales.x.min = 'Minggu 7';
    chart.options.scales.x.max = 'Minggu 16';
    showToast('🌸 Menampilkan Fase Generatif & Pembungaan (Minggu 7 - 16)', 'info');
  } else {
    delete chart.options.scales.x.min;
    delete chart.options.scales.x.max;
    showToast('📊 Menampilkan Seluruh Siklus Pertumbuhan', 'info');
  }
  chart.update();
};

// =====================================================================
// COMMAND PALETTE (CTRL + K)
// =====================================================================
window.setupCommandPalette = function() {
  window.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      window.openCommandPalette();
    }
    if (e.key === 'Escape') {
      const modal = document.getElementById('cmdPaletteModal');
      if (modal && modal.classList.contains('active')) {
        modal.classList.remove('active');
      }
    }
  });
};

window.openCommandPalette = function() {
  const modal = document.getElementById('cmdPaletteModal');
  const input = document.getElementById('cmdSearchInput');
  if (modal) {
    modal.classList.add('active');
    if (input) {
      input.value = '';
      input.focus();
      window.filterCommandPalette('');
    }
  }
};

window.closeCommandPalette = function(e) {
  const modal = document.getElementById('cmdPaletteModal');
  if (modal) modal.classList.remove('active');
};

window.filterCommandPalette = function(query) {
  const list = document.getElementById('cmdResultsList');
  if (!list) return;

  const defaultCommands = [
    { title: '📈 Input Pertumbuhan Mingguan', desc: 'Buka modal input data tinggi, daun, & diameter', action: () => openModal('growthModal') },
    { title: '🌱 Buat Batch Tanam Baru', desc: 'Daftarkan siklus tanam baru ke database', action: () => openModal('batchModal') },
    { title: '🏠 Buka Kalkulator Populasi House', desc: 'Kalkulator teknis geometri & baris tanam', action: () => openModal('houseCalcModal') },
    { title: '📦 Input Hasil Panen', desc: 'Catat tangkai panen, omset, dan rincian grade', action: () => openModal('harvestModal') },
    { title: '🔔 Konfigurasi WhatsApp Webhook', desc: 'Atur notifikasi pengingat ke petani', action: () => openModal('webhookModal') },
    { title: '📥 Export Seluruh Data Pertumbuhan CSV', desc: 'Unduh file CSV riwayat pengukuran', action: () => document.getElementById('exportGrowthCsvBtn')?.click() },
    { title: '🏛️ Digital Twin House 1', desc: 'Lihat denah 12 bedengan House 1', action: () => window.switchDtHouse('House 1') },
    { title: '🏛️ Digital Twin House 2', desc: 'Lihat denah 12 bedengan House 2', action: () => window.switchDtHouse('House 2') }
  ];

  // Also include active batches in search
  const batchCommands = (state.batches || []).map(b => ({
    title: `🌸 Batch ${b.batch_code} (${b.variety_name})`,
    desc: `${b.house_name || 'House 1'} • Tanam ${formatDate(b.planting_date)} • ${fmtNumber(b.plant_count)} tan`,
    action: () => {
      window.openGrowthForBatch(b.id);
    }
  }));

  const all = [...defaultCommands, ...batchCommands];
  const q = (query || '').toLowerCase().trim();
  const matched = q ? all.filter(c => c.title.toLowerCase().includes(q) || c.desc.toLowerCase().includes(q)) : all;

  list.innerHTML = matched.map((item, idx) => `
    <li class="cmd-item" onclick="executeCmdItem(${idx})">
      <div>
        <strong style="display:block;color:#fff;margin-bottom:2px;">${item.title}</strong>
        <span style="font-size:11px;color:var(--text-muted);">${item.desc}</span>
      </div>
      <span style="font-size:11px;color:var(--emerald-400);font-weight:600;">Pilih ↵</span>
    </li>
  `).join('');

  window._activeCmds = matched;
};

window.executeCmdItem = function(index) {
  if (window._activeCmds && window._activeCmds[index]) {
    const cmd = window._activeCmds[index];
    const modal = document.getElementById('cmdPaletteModal');
    if (modal) modal.classList.remove('active');
    cmd.action();
  }
};

// =====================================================================
// TABLE COLUMN SORTING
// =====================================================================
let sortState = { growthCol: -1, growthAsc: true };

window.sortTable = function(tableType, colIndex) {
  if (tableType === 'growth') {
    const records = [...(state.growthRecords || [])];
    if (!records.length) return;

    if (sortState.growthCol === colIndex) {
      sortState.growthAsc = !sortState.growthAsc;
    } else {
      sortState.growthCol = colIndex;
      sortState.growthAsc = true;
    }

    records.sort((a, b) => {
      let valA, valB;
      if (colIndex === 0) { valA = a.batch_code || ''; valB = b.batch_code || ''; }
      else if (colIndex === 1) { valA = a.variety_name || ''; valB = b.variety_name || ''; }
      else if (colIndex === 2) { valA = a.week_number || 0; valB = b.week_number || 0; }
      else if (colIndex === 3) { valA = a.record_date || ''; valB = b.record_date || ''; }
      else if (colIndex === 4) { valA = a.plant_height_cm || 0; valB = b.plant_height_cm || 0; }
      else if (colIndex === 6) { valA = a.health_score || 0; valB = b.health_score || 0; }
      else { valA = 0; valB = 0; }

      if (valA < valB) return sortState.growthAsc ? -1 : 1;
      if (valA > valB) return sortState.growthAsc ? 1 : -1;
      return 0;
    });

    renderGrowthTable(records);
    showToast(`Urutkan kolom ${sortState.growthAsc ? '▲ Menaik' : '▼ Menurun'}`, 'info');
  }
};

// =====================================================================
// CLERK AUTHENTICATION INTEGRATION
// =====================================================================
const CLERK_PUBLISHABLE_KEY = 'pk_test_dm9jYWwtc2Vhc25haWwtNDU0My5jbGVyay5hY2NvdW50cy5kZXYk';

let isClerkInitialized = false;

window.initClerkAuth = async function() {
  if (isClerkInitialized && window.Clerk && window.Clerk.loaded) {
    updateClerkAuthUI();
    return;
  }

  try {
    // Wait for Clerk SDK on window (loaded via script tag in head)
    let retries = 0;
    while (!window.Clerk && retries < 40) {
      await new Promise(r => setTimeout(r, 100));
      retries++;
    }

    if (!window.Clerk) {
      console.warn('⚠️ Clerk SDK belum terdeteksi. Mencoba memuat fallback...');
      await loadClerkScript(CLERK_PUBLISHABLE_KEY);
    }

    if (window.Clerk) {
      if (!window.Clerk.loaded) {
        await window.Clerk.load({
          appearance: {
            variables: {
              colorPrimary: '#10b981',
              colorBackground: '#0b1120',
              colorText: '#f8fafc',
              colorInputBackground: '#162035',
              colorInputText: '#ffffff',
              borderRadius: '12px'
            },
            elements: {
              card: {
                backgroundColor: '#0b1120',
                border: '1px solid rgba(255, 255, 255, 0.12)',
                boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.7)'
              },
              modalBackdrop: {
                backdropFilter: 'blur(8px)',
                backgroundColor: 'rgba(5, 10, 20, 0.75)'
              }
            }
          }
        });
      }

      isClerkInitialized = true;
      updateClerkAuthUI();

      // Listen for auth state changes (login, logout, session switch)
      window.Clerk.addListener(({ user, session }) => {
        updateClerkAuthUI();
      });
    }
  } catch (err) {
    console.error('Clerk Auth initialization error:', err);
  }
};

function updateClerkAuthUI() {
  const authGate = document.getElementById('authGateScreen');
  const mainApp = document.getElementById('mainDashboardApp');
  const btn = document.getElementById('clerkSignInBtn');
  const userBtnContainer = document.getElementById('clerkUserButton');
  const mountDiv = document.getElementById('clerkSignInMount');

  if (window.Clerk && window.Clerk.user) {
    // 1. User IS LOGGED IN — Unlock Dashboard
    state.clerkUser = window.Clerk.user;
    window.Clerk.session?.getToken().then(t => {
      state.clerkToken = t;
    });

    // Hide Auth Gate Screen with smooth fade
    if (authGate) {
      authGate.classList.add('hidden');
      setTimeout(() => {
        authGate.style.display = 'none';
      }, 400);
    }

    // Show Main Dashboard
    if (mainApp) {
      mainApp.style.display = 'block';
    }

    // Mount User Button in Header
    if (btn) btn.style.display = 'none';
    if (userBtnContainer) {
      userBtnContainer.style.display = 'inline-flex';
      userBtnContainer.style.alignItems = 'center';
      if (!userBtnContainer.hasChildNodes()) {
        window.Clerk.mountUserButton(userBtnContainer, {
          appearance: {
            variables: {
              colorPrimary: '#10b981',
              colorBackground: '#0b1120',
              colorText: '#f8fafc'
            }
          }
        });
      }
    }

    // Start Dashboard analytics & simulation
    startAppWhenAuthenticated();

    const fullName = window.Clerk.user.fullName || window.Clerk.user.primaryEmailAddress?.emailAddress || 'Petani Krisan';
    console.log(`✅ Clerk Auth aktif: ${fullName}`);
  } else {
    // 2. User is NOT LOGGED IN — Lock Dashboard & Show Auth Gate
    state.clerkUser = null;
    state.clerkToken = null;

    // Keep dashboard completely hidden
    if (mainApp) {
      mainApp.style.display = 'none';
    }

    // Show Auth Gate Screen
    if (authGate) {
      authGate.style.display = 'flex';
      authGate.classList.remove('hidden');
    }

    if (btn) {
      btn.style.display = 'inline-flex';
      const btnText = document.getElementById('clerkBtnText');
      if (btnText) btnText.textContent = 'Masuk (Clerk)';
    }
    if (userBtnContainer) {
      userBtnContainer.style.display = 'none';
    }

    // Mount Native Clerk Sign-In component into Auth Gate
    if (mountDiv && window.Clerk) {
      const loadingState = document.getElementById('clerkLoadingState');
      if (loadingState) loadingState.style.display = 'none';

      if (!mountDiv.querySelector('.cl-signIn-root')) {
        mountDiv.innerHTML = '';
        window.Clerk.mountSignIn(mountDiv, {
          appearance: {
            variables: {
              colorPrimary: '#10b981',
              colorBackground: '#0b1120',
              colorText: '#f8fafc',
              colorInputBackground: '#162035',
              colorInputText: '#ffffff',
              borderRadius: '12px'
            },
            elements: {
              card: {
                backgroundColor: 'transparent',
                border: 'none',
                boxShadow: 'none'
              },
              footer: {
                background: 'transparent'
              }
            }
          }
        });
      }
    }
  }
}

function loadClerkScript(publishableKey) {
  return new Promise((resolve, reject) => {
    if (window.Clerk) return resolve();
    const script = document.createElement('script');
    script.src = 'https://vocal-seasnail-4543.clerk.accounts.dev/npm/@clerk/clerk-js@5/dist/clerk.browser.js';
    script.async = true;
    script.crossOrigin = 'anonymous';
    script.setAttribute('data-clerk-publishable-key', publishableKey);
    script.onload = () => resolve();
    script.onerror = (e) => reject(new Error('Gagal memuat Clerk JS'));
    document.head.appendChild(script);
  });
}

window.handleClerkLogin = function() {
  if (window.Clerk) {
    if (window.Clerk.user) {
      window.Clerk.openUserProfile({
        appearance: {
          variables: {
            colorPrimary: '#10b981',
            colorBackground: '#0b1120',
            colorText: '#f8fafc'
          }
        }
      });
    } else {
      window.Clerk.openSignIn({
        appearance: {
          variables: {
            colorPrimary: '#10b981',
            colorBackground: '#0b1120',
            colorText: '#f8fafc',
            colorInputBackground: '#162035',
            colorInputText: '#ffffff',
            borderRadius: '12px'
          },
          elements: {
            card: {
              backgroundColor: '#0b1120',
              border: '1px solid rgba(255, 255, 255, 0.12)',
              boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.7)'
            }
          }
        }
      });
    }
  } else {
    showToast('⏳ Mempersiapkan Clerk Login...', 'info');
    window.initClerkAuth().then(() => {
      if (window.Clerk) {
        window.Clerk.openSignIn();
      } else {
        showToast('Gagal memuat modul login. Periksa koneksi internet.', 'error');
      }
    });
  }
};

// Also listen to window load event to ensure Clerk initializes smoothly
window.addEventListener('load', () => {
  if (window.initClerkAuth) window.initClerkAuth();
});



