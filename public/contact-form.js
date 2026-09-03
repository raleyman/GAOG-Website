document.addEventListener('DOMContentLoaded', () => {
  var f = document.getElementById('contact-form');
  if (!f) return;

  var submitBtn = f.querySelector('button[type="submit"]');
  var defaultNote = document.getElementById('form-note-default');
  var successMsg = document.getElementById('form-success');
  var errorMsg = document.getElementById('form-error');

  f.addEventListener('submit', (e) => {
    e.preventDefault();

    successMsg.hidden = true;
    errorMsg.hidden = true;

    var formData = new FormData(f);
    var topic = document.getElementById('topic').value;
    formData.set('subject', `New Consulting Inquiry: ${topic || 'General'} — GAOG Website`);

    var originalText = submitBtn.textContent;
    submitBtn.textContent = 'Sending…';
    submitBtn.disabled = true;

    fetch('https://api.web3forms.com/submit', {
      method: 'POST',
      body: formData,
      headers: { Accept: 'application/json' },
    })
      .then((response) => response.json().then((data) => ({ ok: response.ok, data: data })))
      .then((result) => {
        if (result.ok && result.data?.success) {
          f.reset();
          defaultNote.hidden = true;
          successMsg.hidden = false;
        } else {
          errorMsg.hidden = false;
        }
      })
      .catch(() => {
        errorMsg.hidden = false;
      })
      .then(() => {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
      });
  });
});
