const API_URL        = 'http://localhost:8001/api/news';
const N8N_WEBHOOK    = 'http://localhost:5678/webhook/cyber-news';
const RENDER_URL     = 'http://localhost:8002/render';
const DISPATCHER_URL = 'http://localhost:8080/app/v1';

let globalNewsData = [];//buffering webcrawing news
let pendingHtml = null;// buffering the render template from render service



// <<feed the news from RSS>>
//globalNewsData :Array = buffer parse { data } ,  if news added(existed in queue) render the blue border
async function loadFeed() {
    try {
        const res = await fetch(API_URL);
        if (!res.ok) throw new Error('API ERROR');
        const { data } = await res.json();
        globalNewsData = data;

        if (data.length === 0) {
            feed.innerHTML = '<div class="loading">No alerts yet.</div>';
            return;
        }

        const queue = getQueue();
        const queueUrls = queue.map(e => e.url);

        document.getElementById('feed').innerHTML = data.map((item, index) => {
            const tags = (item.categories || item.categoies || []).map(t => `<span class="tag">${t}</span>`).join('');
            const inQueue = queueUrls.includes(item.link);
            const queueNum = inQueue ? queueUrls.indexOf(item.link) + 1 : '';
            return `
                <div class="card ${inQueue ? 'in-queue' : ''}" onclick="openNewsModal(${index})">
                    <div class="queue-badge">${queueNum}</div>
                    <div class="tag-container">${tags}</div>
                    <div class="title">${item.title}</div>
                    <div class="summary">${item.summary}</div>
                </div>`;
        }).join('');

        document.getElementById('statusText').innerText = `Live Threat Feed • ${data.length} Alerts Active`;
        updateQueueBar();
    } catch (err) {
        console.error(err);
        document.getElementById('statusText').innerText = 'Live Threat Feed • Connection Offline';
        document.getElementById('statusText').style.color = '#ff4d4d';
    }
}


//<<Queue>>: array = CRUD for loaclstorage
//updateQueueBar(): 
// for i = 0 to 2:if queue[i] show '✓' else show No.(1./2./3., innerText = i+1)
// switch const: case: 0 or 1: 'add news(n/3)' case 2: 'add news&dispatch (3/3)' case <= 3 :disable  


function getQueue() {
    return JSON.parse(localStorage.getItem('digestQueue') || '[]');
}
function saveQueue(q) {
    localStorage.setItem('digestQueue', JSON.stringify(q));
}
function clearQueue() {
    if (!confirm('clean queue？')) return;
    localStorage.removeItem('digestQueue');
    loadFeed();
}
function updateQueueBar() {
    const queue = getQueue();
    for (let i = 0; i < 3; i++) {
        const slot = document.getElementById(`slot${i}`);
        if (queue[i]) {
            slot.classList.add('filled');
            slot.innerText = '✓';
            slot.title = queue[i].title[0] || '';
        } else {
            slot.classList.remove('filled');
            slot.innerText = i + 1;
            slot.title = '';
        }
    }
    // update add button label
    const btn = document.getElementById('addToQueueBtn');
    if (btn) {
        const count = queue.length;
        if (count >= 3) {
            btn.innerText = 'already 3 alerts';
            btn.disabled = true;
        } else if (count === 2) {
            btn.innerText = `add news & dispatch (3/3)`;
            btn.disabled = false;
        } else {
            btn.innerText = `add news (${count + 1}/3)`;
            btn.disabled = false;
        }
    }
}



//<<News preview>>:RSS card preview
//openNewsModel(idx): 
// for tag, title, summary, link: doc.getElement.innertext = item.element
// click analyzeBtn triggerAnalysis(item.link)
//closeNewsModel(): remove 'active class'
function openNewsModal(index) {
    const item = globalNewsData[index];
    if (!item) return;
    const tags = (item.categories || item.categoies || []).map(t => `<span class="tag">${t}</span>`).join('');
    document.getElementById('modalTags').innerHTML = tags;
    document.getElementById('modalTitle').innerText = item.title;
    document.getElementById('modalSummary').innerText = item.summary;
    document.getElementById('modalSourceLink').href = item.link;

    const btn = document.getElementById('analyzeBtn');
    btn.innerHTML = 'Analyze and Generate Digest';
    btn.disabled = false;
    btn.onclick = () => triggerAnalysis(item.link);

    document.getElementById('newsModal').classList.add('active');
}
function closeNewsModal(e) {
    if (e) e.preventDefault();
    document.getElementById('newsModal').classList.remove('active');
}

//<<trigger analysis>>
// await fetch(n8n api + news url)
//  -> json: { data: { title, keywords, date[], scope[], impact[], summary[], url }, similarity: {...} }
async function triggerAnalysis(url) {
    const btn = document.getElementById('analyzeBtn');
    if (!url || !url.startsWith('http')) { alert('Invalid URL'); return; }

    btn.innerHTML = '⏳ Analyzing...';
    btn.disabled = true;

    try {
        const finalUrl = `${N8N_WEBHOOK}?NewsUrl=${encodeURIComponent(url)}`;
        const res = await fetch(finalUrl);
        if (!res.ok) throw new Error('n8n error: ' + res.status);
        const json = await res.json();

        closeNewsModal(null);
        openDigestModal(json);
    } catch (err) {
        alert('Analysis failed:\n' + err.message);
        btn.innerHTML = 'Analyze and Generate Digest';
        btn.disabled = false;
}
}

//<<Digest editor>>
// openDigestModel(json): for element in json: put in <textarea>(d_title, d_scope, d_impact, d_summary, d_url)
// renderSimilarityChart: let similarity : sort top20 and rendering
function openDigestModal(json) {
    const d = json.data || {};
    const sim = json.similarity || {};

    document.getElementById('d_title').value   = d.title   || '';
    document.getElementById('d_date').value    = (d.date   || []).join('\n');
    document.getElementById('d_scope').value   = (d.scope  || []).join('\n');
    document.getElementById('d_impact').value  = (d.impact || []).join('\n');
    document.getElementById('d_summary').value = (d.summary|| []).join('\n');
    document.getElementById('d_url').value     = d.url     || '';

    renderSimilarityChart(sim);
    updateQueueBar();
    document.getElementById('digestModal').classList.add('active');
}
function closeDigestModal(e) {
    if (e) e.preventDefault();
    document.getElementById('digestModal').classList.remove('active');
}
function renderSimilarityChart(scores) {
    const container = document.getElementById('similarityChart');
    if (!scores || Object.keys(scores).length === 0) {
        container.innerHTML = '<div style="color:var(--text-muted);font-size:13px;">No similarity data</div>';
        return;
    }
    const sorted = Object.entries(scores).sort((a, b) => b[1] - a[1]).slice(0, 20);
    container.innerHTML = sorted.map(([name, score]) => {
        const high = score > 0.5;
        const color = high ? 'var(--success)' : 'var(--text-secondary)';
        const bar   = high ? 'var(--success)' : 'var(--accent)';
        return `
        <div class="customer-card">
            <div class="label-row">
                <span class="label-name">${name}</span>
                <span style="color:${color};font-weight:600;">${(score*100).toFixed(2)}%</span>
            </div>
            <div class="progress-container">
                <div class="progress-fill" style="width:${score*100}%;background:${bar}"></div>
            </div>
        </div>`;
    }).join('');
}


//<<payload collection>>
// collectpayload(): for each field: {field: lines(d_field)}
function collectPayload() {
    const lines = (id) => document.getElementById(id).value
        .split('\n').map(l => l.trim()).filter(Boolean);
    return {
        title:   [document.getElementById('d_title').value.trim()],
        date:    lines('d_date'),
        scope:   lines('d_scope'),
        impact:  lines('d_impact'),
        summary: lines('d_summary'),
        url:     document.getElementById('d_url').value.trim() || '#',
    };
}
function copyDigest() {
    const p = collectPayload();
    const text = `標題: ${p.title[0]}\n\n發生時間:\n${p.date.join('\n')}\n\n影響範圍:\n${p.scope.join('\n')}\n\n潛在影響:\n${p.impact.join('\n')}\n\n重點整理:\n${p.summary.join('\n')}\n\n網址: ${p.url}`;
    navigator.clipboard.writeText(text).then(() => alert('Copied!'));
}

//<<AddToQueue>>: enqueue(payload:collectpayload())
// payload -> enqueue -> savequeue
// if Q.length <3:
//  closeDigestmodel; loadfeed();
// otherwise Q.length == 3:
//  html <- rendering(POST/render body: event{queue})
//  pendingHtml = html
//  openPriewModal(html)
async function addToQueue() {
    const payload = collectPayload();
    if (!payload.title[0]) { alert('title can not be NULL！'); return; }

    const queue = getQueue();
    if (queue.length >= 3) { alert('Queue Full'); return; }

    queue.push(payload);
    saveQueue(queue);

    if (queue.length < 3) {
        // 前兩篇：存完關 modal，更新 UI
        closeDigestModal(null);
        loadFeed();
        return;
    }

    //3nd news render+preview
    const btn = document.getElementById('addToQueueBtn');
    btn.innerHTML = '⏳ Rendering...';
    btn.disabled = true;

    try {
        const renderRes = await fetch(RENDER_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ events: queue })
        });
        if (!renderRes.ok) throw new Error('Render failed: ' + renderRes.status);
        const { html } = await renderRes.json();

        pendingHtml = html;
        closeDigestModal(null);
        openPreviewModal(html);

        btn.innerHTML = 'add news & dispatch (3/3)';
        btn.disabled = false;
    } catch (err) {
        alert('Render fail：\n' + err.message);
        queue.pop();
        saveQueue(queue);
        updateQueueBar();
        btn.innerHTML = 'add news & dispatch (3/3)';
        btn.disabled = false;
    }
}


//<<PreviewModal>>
// openPreviewModal(html) : <iframe id = prefiewFrame>.srcdoc = html
function openPreviewModal(html) {
    document.getElementById('previewFrame').srcdoc = html;
    document.getElementById('previewModal').classList.add('active');
}
function closePreviewModal(e) {
    if (e) e.preventDefault();
    document.getElementById('previewModal').classList.remove('active');
}
async function confirmDispatch() {
    if (!pendingHtml) return;
    const btn = document.getElementById('confirmDispatchBtn');
    btn.innerHTML = '⏳ Dispatching...';
    btn.disabled = true;
    try {
        const dispatchRes = await fetch(DISPATCHER_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ html: pendingHtml })
        });
        if (!dispatchRes.ok) throw new Error('Dispatch failed: ' + dispatchRes.status);
        pendingHtml = null;
        localStorage.removeItem('digestQueue');
        alert('dispatch successful！');
        closePreviewModal(null);
        loadFeed();
    } catch (err) {
        alert('Dispatch fail：\n' + err.message);
        btn.innerHTML = 'confirm to dispatch';
        btn.disabled = false;
    }
}


//<<setting RSS source>>
//togglesetting(): show the RSS source setting panel
//refreshSourceList: get the RSS source from mongoDB(await fetch('http://localhost:8001/api/rss-source'))
// addNewRss(): POST /api/rss-source{url}
// deleteSource(url): DELETE /api/rss-source{url}
function toggleSettings() {
    const panel = document.getElementById('settingsPanel');
    panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
    if (panel.style.display === 'block') refreshSourceList();
}
async function refreshSourceList() {
    const listDiv = document.getElementById('sourceList');
    try {
        const res = await fetch('http://localhost:8001/api/rss-sources');
        const data = await res.json();
        listDiv.innerHTML = data.map(src => `
            <div style="display:flex;justify-content:space-between;align-items:center;padding:12px 0;border-bottom:1px solid var(--border);">
                <span style="font-size:14px;color:var(--text-secondary);overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:70%;">${src.url}</span>
                <button onclick="deleteSource('${src.url}')" style="width:auto;padding:6px 12px;background:#3d1c1c;border:none;color:white;border-radius:4px;font-size:12px;cursor:pointer;">Delete</button>
            </div>`).join('') || '<div style="color:var(--text-muted)">No sources configured.</div>';
    } catch (err) {
        listDiv.innerHTML = '<div style="color:var(--danger)">Failed to load sources.</div>';
    }
}
async function addNewRss() {
    const input = document.getElementById('newRssUrl');
    const url = input.value.trim();
    if (!url || !url.startsWith('http')) { alert('Invalid HTTP/HTTPS URL'); return; }
    try {
        const res = await fetch('http://localhost:8001/api/rss-sources', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
        });
        const result = await res.json();
        if (result.status === 'success') { alert('Added!'); input.value = ''; refreshSourceList(); }
        else alert('Failed: ' + result.message);
    } catch (err) { alert('API connection failed'); }
}
async function deleteSource(url) {
    if (!confirm('Remove this source?')) return;
    try {
        const res = await fetch('http://localhost:8001/api/rss-sources', {
            method: 'DELETE',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
        });
        if (res.ok) refreshSourceList();
    } catch (err) { alert('Delete failed'); }
}

// ===== INIT =====
loadFeed();
setInterval(loadFeed, 30000);