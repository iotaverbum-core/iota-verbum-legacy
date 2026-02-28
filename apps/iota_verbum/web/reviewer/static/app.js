(async function(){
  const el = document.getElementById('app');
  try{
    const r = await fetch('/cache'); const j = await r.json();
    el.innerText = JSON.stringify(j,null,2);
  }catch(e){ el.innerText = 'No cache available.' }
})();