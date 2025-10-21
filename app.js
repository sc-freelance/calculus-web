document.getElementById('calc-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    const expr = document.getElementById('expr').value;
    const operation = document.getElementById('operation').value;

    let endpoint = '/' + operation.replace(/\s+/g, '_').toLowerCase();

    const response = await fetch(endpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ expr: expr })
    });

    const data = await response.json();
    document.getElementById('result').textContent = data.latex || data.error || "No result";
})

document.getElementById('result').innerHTML = `\\(${data.latex}\\)`;
if (window.MathJax) MathJax.typesetPromise();