function toggleAddBox(button) {
    const form = button.nextElementSibling;
    if (form) {
        if (form.style.display == 'none') {
            form.style.display = 'block';
        }
        else {
            form.style.display = 'none';
        }
    }
}
    

function toggleEditBox(button) {
    const form = button.nextElementSibling;
    if (form) {
        if (form.style.display == 'none') {
            form.style.display = 'block';
        }
        else {
            form.style.display = 'none';
        }
    }
}

function toggleEditNote(button) {
    const form = button.previousElementSibling;
    if (form) {
        if (form.style.display == 'none') {
                form.style.display = 'block';
            }
        else {
            form.style.display = 'none';
        }
    }
}
