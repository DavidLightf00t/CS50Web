document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  document.querySelector('#button').addEventListener('click', (event) => {
    event.preventDefault();

    var recipient = document.querySelector('#compose-recipients').value;
    var subject = document.querySelector('#compose-subject').value;
    var body = document.querySelector('#compose-body').value;
  
    console.log("Recipient");
  
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
          recipients: recipient,
          subject: subject,
          body: body
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    })
    .catch(event => {
      console.error('Error:', error);
    });
    
  })
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views

  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#mail-contents').style.display = 'none'

  // Show the mailbox name
  document.querySelector('#mailbox-name').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;
  if(mailbox == "inbox"){
    console.log(mailbox == "inbox");

    // Fetch emails
    fetch('/emails/inbox')
    .then(response => response.json())
    .then(emails => {
      // Print emails
      // console.log(emails)
      const mail_container = document.querySelector('#mail-container');
      mail_container.innerHTML = '';

      emails.forEach(email => {
        if(email.read == true){
          document.querySelector('#mail-container').style.background_color = 'lightgrey';  
        }

        if(email.archived == false){
          const email_contents = document.createElement('div');
          email_contents.dataset.id = email.id;

          email_contents.innerHTML = `
          <div id="mail" class="mail">
            <div class="sender-wrapper-left">
              <div class="sender"><strong>${email.sender}</strong></div>
            </div>
            <div class="subject-wrapper-left">
              <div class="subject">${email.subject}</div>
            </div>
            <div class="timestamp-wrapper-right">
              <div class="timestamp">${email.timestamp}</div>
            </div>
          </div>
          `;

          // When email is clicked on
          email_contents.addEventListener('click', () => {
            document.querySelector('#mail-container').innerHTML = '';
            document.querySelector('#mailbox-name').innerHTML = '';

            const email_id = email_contents.dataset.id;
            load_email_contents(email_id);
          })

          mail_container.appendChild(email_contents)
        }
      });
    })
    .catch(error => console.error('Error:', error));

  }

  if(mailbox == "sent"){
    const mail_container = document.querySelector('#mail-container');
    mail_container.innerHTML = '';
    console.log("Mailbox", mailbox == "sent");
  }

  if(mailbox == "archive"){
    const mail_container = document.querySelector('#mail-container');
    mail_container.innerHTML = '';
    console.log("Archived", mailbox == "archive");
  }
}

function load_email_contents(email_id){
  document.querySelector('#mail-contents').style.display = 'block'

  console.log(email_id)
  
  fetch(`/emails/${email_id}`, {
    method: 'PUT',
    body: JSON.stringify({
        read: true
    })
  })
  

  fetch(`/emails/${email_id}`)
  .then(response => response.json())
  .then(email => {
      console.log(email);
      document.querySelector('#from-info').innerHTML = `<strong>From: </strong> ${email.sender}`;
      document.querySelector('#to-info').innerHTML = `<strong>To: </strong> ${email.recipients}`;
      document.querySelector('#subject-info').innerHTML = `<strong>Subject: </strong> ${email.subject}`;
      document.querySelector('#timestamp-info').innerHTML = `<strong>Timestamp: </strong> ${email.timestamp}`;

      document.querySelector('#body-info').innerHTML = `${email.body}`;
  });
}