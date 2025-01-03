// defines the delete note function which is used in views.py


function deleteNote(noteId) {
    // sends a fetch request to the delete-note route defined in views.py
    fetch('/delete-note', {
        method: 'POST',
        // sends the noteId as a JSON payload
        body: JSON.stringify({ noteId: noteId }),
        // sets the content type header to application/json to indicate that
        // the request contains JSON data. 
        headers: { 'Content-Type': 'application/json' }
    // after the server processes the request, redirects to homepage.  
    }).then((_res) => {
        window.location.href = '/';
    });
}
