document.addEventListener('DOMContentLoaded', function () {
  var f = document.getElementById('contact-form');
  if (!f) return;

  var submitBtn = f.querySelector('button[type="submit"]');
  var defaultNote = document.getElementById('form-note-default');
  var successMsg = document.getElementById('form-success');
  var errorMsg = document.getElementById('form-error');

  f.addEventListener('submit', function (e) {
    e.preventDefault();

    successMsg.hidden = true;
    errorMsg.hidden = true;

    var formData = new FormData(f);
    var topic = document.getElementById('topic').value;
    formData.set('subject', 'New Consulting Inquiry: ' + (topic || 'General') + ' — GAOG Website');

    var originalText = submitBtn.textContent;
    submitBtn.textContent = 'Sending…';
    submitBtn.disabled = true;

    fetch('https://api.web3forms.com/submit', {
      method: 'POST',
      body: formData,
      headers: { Accept: 'application/json' },
    })
      .then(function (response) {
        return response.json().then(function (data) {
          return { ok: response.ok, data: data };
        });
      })
      .then(function (result) {
        if (result.ok && result.data && result.data.success) {
          f.reset();
          defaultNote.hidden = true;
          successMsg.hidden = false;
        } else {
          errorMsg.hidden = false;
        }
      })
      .catch(function () {
        errorMsg.hidden = false;
      })
      .then(function () {
        submitBtn.textContent = originalText;
        submitBtn.disabled = false;
      });
  });
});
