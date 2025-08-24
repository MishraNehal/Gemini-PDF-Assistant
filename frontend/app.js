const API_BASE = "http://localhost:8000";

let sessionId = null;

const el = {
  pdfs: document.getElementById('pdfs'),
  uploadBtn: document.getElementById('uploadBtn'),
  askBtn: document.getElementById('askBtn'),
  resetBtn: document.getElementById('resetBtn'),
  question: document.getElementById('question'),
  chat: document.getElementById('chatWindow'),
  status: document.getElementById('status'),
};

function addMsg(text, who='bot'){
  const div = document.createElement('div');
  div.className = `msg ${who}`;
  div.textContent = text;
  el.chat.appendChild(div);
  el.chat.scrollTop = el.chat.scrollHeight;
}

function addSources(sources){
  if(!sources || !sources.length) return;
  const wrap = document.createElement('div');
  wrap.className = 'source';
  wrap.textContent = "Sources: " + sources.map(s => {
    const src = s.source ? s.source.split('/').pop() : 'PDF';
    const page = (s.page !== undefined && s.page !== null) ? ` p.${s.page}` : '';
    return `${src}${page}`;
  }).join(' • ');
  el.chat.appendChild(wrap);
  el.chat.scrollTop = el.chat.scrollHeight;
}

async function uploadPDFs(){
  const files = el.pdfs.files;
  if(!files.length){
    el.status.textContent = "Please choose at least one PDF.";
    return;
  }
  el.status.textContent = "Indexing PDFs...";
  el.uploadBtn.disabled = true;

  const form = new FormData();
  for(const f of files){
    form.append('files', f);
  }
  try {
    const res = await fetch(`${API_BASE}/upload`, {method:'POST', body: form});
    const data = await res.json();
    if(!res.ok){
      throw new Error(data.error || 'Upload failed');
    }
    sessionId = data.session_id;
    el.status.textContent = "Indexed ✔ Ready to chat.";
    addMsg("Your PDFs are indexed. Ask me anything about them!");
  } catch (e){
    console.error(e);
    el.status.textContent = "Error: " + e.message;
  } finally {
    el.uploadBtn.disabled = false;
  }
}

async function ask(){
  const q = el.question.value.trim();
  if(!q) return;
  if(!sessionId){
    addMsg("Please upload PDFs first.", 'bot');
    return;
  }
  addMsg(q, 'user');
  el.question.value = "";
  el.askBtn.disabled = true;

  try {
    const res = await fetch(`${API_BASE}/ask`, {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({session_id: sessionId, question: q})
    });
    const data = await res.json();
    if(!res.ok){
      throw new Error(data.error || 'Ask failed');
    }
    addMsg(data.answer || "(no answer)");
    addSources(data.sources || []);
  } catch (e){
    console.error(e);
    addMsg("Error: " + e.message);
  } finally {
    el.askBtn.disabled = false;
  }
}

async function reset(){
  if(!sessionId) return;
  try {
    await fetch(`${API_BASE}/reset`, {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({session_id: sessionId})
    });
    addMsg("Chat history cleared for this session.");
  } catch (e){
    console.error(e);
  }
}

el.uploadBtn.addEventListener('click', uploadPDFs);
el.askBtn.addEventListener('click', ask);
el.resetBtn.addEventListener('click', reset);
el.question.addEventListener('keydown', (e)=>{
  if(e.key === 'Enter') ask();
});
