document.getElementById('generateButton').addEventListener('click', function() {
  const keyword = document.getElementById('userPrompt').value;
  const contentType = document.getElementById('format').value;
  const tone = document.getElementById('tone').value;

  // Make an API call to the backend
  fetch('/generate', {
      method: 'POST',
      headers: {
          'Content-Type': 'application/json'
      },
      body: JSON.stringify({ keyword: keyword, contentType: contentType, tone: tone })
  })
  .then(response => response.json())
  .then(data => {
      // Display the generated content
      let outputHtml = '';
      data.articles.forEach(article => {
          outputHtml += `<div class="article">`;
          outputHtml += `<h3>${article.title}</h3>`;
          outputHtml += `<p>Published Date: ${article.published_date || 'N/A'}</p>`;
          outputHtml += `<p>Source: ${article.source_name || 'N/A'}</p>`;
          outputHtml += `<p>Link: <a href="${article.url}" target="_blank">${article.url}</a></p>`;
          outputHtml += `<p>Generated Content: ${article.summary || 'No content available.'}</p>`;
          outputHtml += `</div>`;
      });
      document.getElementById('outputDisplay').innerHTML = outputHtml; // Use innerHTML for HTML content
      document.querySelector('.output-section').style.display = 'block'; // Show output section
  })
  .catch(error => console.error('Error:', error));
});

// Tab functionality
const tabs = document.querySelectorAll('.tab');
tabs.forEach(tab => {
  tab.addEventListener('click', function() {
      const format = this.id.replace('Tab', ''); // Get format from tab ID
      document.getElementById('outputDisplay').innerText = `Displaying ${format} content...`;
  });
});